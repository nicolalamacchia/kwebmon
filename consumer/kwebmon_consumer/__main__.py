import argparse
import logging
import os
import sys

from kwebmon_consumer.consumer import Consumer, InvalidMessageReceivedError
from kwebmon_consumer.storage import PostgresStorage

DEFAULT_KAFKA_CA = "kafka-ca.pem"
DEFAULT_KAFKA_CERT = "kafka-service.cert"
DEFAULT_KAFKA_KEY = "kafka-service.key"
DEFAULT_KAFKA_TOPIC = "kwebmon"
DEFAULT_KAFKA_GROUP_ID = "kwebmon-consumer"
DEFAULT_POSTGRES_TABLE_NAME = "kwebmon_metrics"

KAFKA_CA_ENV_VAR = "KWEBMON_KAFKA_CA"
KAFKA_CERT_ENV_VAR = "KWEBMON_KAFKA_CERT"
KAFKA_KEY_ENV_VAR = "KWEBMON_KAFKA_KEY"
KAFKA_URI_ENV_VAR = "KWEBMON_KAFKA_URI"
POSTGRES_URI_ENV_VAR = "KWEBMON_POSTGRES_URI"

kafka_ca = os.environ.get(KAFKA_CA_ENV_VAR, DEFAULT_KAFKA_CA)
kafka_cert = os.environ.get(KAFKA_CERT_ENV_VAR, DEFAULT_KAFKA_CERT)
kafka_key = os.environ.get(KAFKA_KEY_ENV_VAR, DEFAULT_KAFKA_KEY)

kafka_uri = os.environ.get(KAFKA_URI_ENV_VAR)
postgres_uri = os.environ.get(POSTGRES_URI_ENV_VAR)

logger = logging.getLogger("kwebmon-consumer")


def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        prog="kwebmon_consumer",
        description=("Receives Kafka messages "
                     "and stores them into a PostgreSQL database."),
        epilog=(
            "NOTE: Some arguments are required if the respective environment "
            "variable is not defined."
        )
    )
    parser.add_argument(
        "--postgres-uri",
        default=postgres_uri,
        help=(
            "PostgreSQL service URI."
            f"Required if the environment variable {POSTGRES_URI_ENV_VAR} "
            "is not defined."
        )
    )
    parser.add_argument(
        "--postgres-table-name",
        default=DEFAULT_POSTGRES_TABLE_NAME,
        help=("PostgreSQL table name to store consumed messages to "
              f"(default: {DEFAULT_POSTGRES_TABLE_NAME}).")
    )
    parser.add_argument(
        "--kafka-uri",
        default=kafka_uri,
        help=(
            "Kafka service URI. "
            f"Required if the environment variable {KAFKA_URI_ENV_VAR} "
            "is not defined."
        )
    )
    parser.add_argument(
        "--kafka-ca",
        default=kafka_ca,
        help=(
            "CA file path for the Kafka service. "
            f"Overrides the environment variable {KAFKA_CA_ENV_VAR} "
            f"(default: {DEFAULT_KAFKA_CA})."
        ),
    )
    parser.add_argument(
        "--kafka-cert",
        default=kafka_cert,
        help=(
            "Certificate file path for the Kafka service. "
            f"Overrides the environment variable {KAFKA_CERT_ENV_VAR} "
            f"(default: {DEFAULT_KAFKA_CERT})."
        )
    )
    parser.add_argument(
        "--kafka-key",
        default=kafka_key,
        help=(
            "Key file path for the Kafka service. "
            f"Overrides the environment variable {KAFKA_KEY_ENV_VAR} "
            f"(default: {DEFAULT_KAFKA_KEY})."
        )
    )
    parser.add_argument(
        "--kafka-topic",
        default=DEFAULT_KAFKA_TOPIC,
        help=(
            f"Kafka topic to send events to (default: {DEFAULT_KAFKA_TOPIC})."
        )
    )
    parser.add_argument(
        "--kafka-group-id",
        default=DEFAULT_KAFKA_GROUP_ID,
        help=f"Kafka consumer group id (default: {DEFAULT_KAFKA_GROUP_ID}).",
    )
    parsed_args = parser.parse_args(args)

    if parsed_args.postgres_uri is None:
        parser.error(
            "--postgres-uri is required if the environment variable "
            f"{POSTGRES_URI_ENV_VAR} is not defined."
        )

    if parsed_args.kafka_uri is None:
        parser.error(
            "--kafka-uri is required if the environment variable "
            f"{KAFKA_URI_ENV_VAR} is not defined."
        )

    return parsed_args


def main():
    args = parse_args()

    logger.info("Initializing Kafka consumer")
    consumer = Consumer(
        args.kafka_uri,
        args.kafka_topic,
        args.kafka_ca,
        args.kafka_cert,
        args.kafka_key,
        args.kafka_group_id,
    )

    logger.info("Initializing storage engine (PostgreSQL database)")
    storage = PostgresStorage(
        args.postgres_uri,
        args.postgres_table_name
    )

    def save(message_key: dict, message_value: dict) -> None:
        logger.info("Storing received key: "
                    f"{message_key}, value: {message_value}")
        storage.save(
            message_key["url"],
            message_value["utc_completed_at"],
            message_key["pattern"],
            message_value.get("is_content_valid"),
            message_value.get("response_time"),
            message_value.get("status_code"),
            message_value.get("error"),
        )

    logger.info("Listening for messages")
    try:
        consumer.listen(save)
    except KeyboardInterrupt:
        logger.warning("Interrupted")
        consumer.close()
    except InvalidMessageReceivedError as invalid_message_err:
        logger.error(invalid_message_err)


if __name__ == "__main__":
    main()
