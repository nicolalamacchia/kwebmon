import argparse
import logging
import sys

from kwebmon.consumer.consumer import Consumer, InvalidMessageReceivedError
from kwebmon.consumer.storage import PostgresStorage

DEFAULT_KAFKA_TOPIC = "kwebmon"
DEFAULT_KAFKA_GROUP_ID = "kwebmon-consumer"
DEFAULT_POSTGRES_TABLE_NAME = "kwebmon_metrics"

logger = logging.getLogger("kwebmon.consumer")


def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--postgres-uri",
        required=True,
        help="PostgreSQL service URI"
    )
    parser.add_argument(
        "--postgres-table-name",
        default=DEFAULT_POSTGRES_TABLE_NAME,
        help=("PostgreSQL table name to store consumed messages to "
              f"(default: {DEFAULT_POSTGRES_TABLE_NAME})")
    )
    parser.add_argument(
        "--kafka-uri",
        required=True,
        help="Kafka service URI",
    )
    parser.add_argument(
        "--kafka-ca",
        required=True,
        help=("CA file path for the Kafka service"),
    )
    parser.add_argument(
        "--kafka-cert",
        required=True,
        help="Certificate file path for the Kafka service",
    )
    parser.add_argument(
        "--kafka-key",
        required=True,
        help="Key file path for the Kafka service",
    )
    parser.add_argument(
        "--kafka-topic",
        default=DEFAULT_KAFKA_TOPIC,
        help=f"Kafka topic to send events to (default: {DEFAULT_KAFKA_TOPIC})",
    )
    parser.add_argument(
        "--kafka-group-id",
        default=DEFAULT_KAFKA_GROUP_ID,
        help=f"Kafka consumer group id (default: {DEFAULT_KAFKA_GROUP_ID})",
    )
    return parser.parse_args(args)


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
