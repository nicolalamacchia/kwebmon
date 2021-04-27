import argparse
import asyncio
import logging
import os
import sys

from kwebmon_producer.producer import Producer
from kwebmon_producer.monitoring import Monitor
from kwebmon_producer.utils import get_sites

DEFAULT_CHECK_INTERVAL = 5

DEFAULT_KAFKA_CA = "kafka-ca.pem"
DEFAULT_KAFKA_CERT = "kafka-service.cert"
DEFAULT_KAFKA_KEY = "kafka-service.key"
DEFAULT_KAFKA_TOPIC = "kwebmon"

KAFKA_CA_ENV_VAR = "KWEBMON_KAFKA_CA"
KAFKA_CERT_ENV_VAR = "KWEBMON_KAFKA_CERT"
KAFKA_KEY_ENV_VAR = "KWEBMON_KAFKA_KEY"
KAFKA_URI_ENV_VAR = "KWEBMON_KAFKA_URI"

kafka_ca = os.environ.get(KAFKA_CA_ENV_VAR, DEFAULT_KAFKA_CA)
kafka_cert = os.environ.get(KAFKA_CERT_ENV_VAR, DEFAULT_KAFKA_CERT)
kafka_key = os.environ.get(KAFKA_KEY_ENV_VAR, DEFAULT_KAFKA_KEY)

kafka_uri = os.environ.get(KAFKA_URI_ENV_VAR)

logger = logging.getLogger("kwebmon-producer")


def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        prog="kwebmon_producer",
        description=("Monitors the websites in the specified configuration "
                     "and sends metrics to a Kafka topic."),
        epilog=(
            "NOTE: Some arguments are required if the respective environment "
            "variable is not defined."
        )
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
        help=f"Kafka topic to send events to (default: {DEFAULT_KAFKA_TOPIC})",
    )
    parser.add_argument(
        "-i",
        "--check-interval",
        default=DEFAULT_CHECK_INTERVAL,
        type=int,
        help=f"Check interval (seconds, default: {DEFAULT_CHECK_INTERVAL})",
    )
    parser.add_argument(
        "-s",
        "--sites-list",
        required=True,
        help="Configuration file (JSON) with a list of websites to monitor",
    )
    parsed_args = parser.parse_args(args)

    if parsed_args.kafka_uri is None:
        parser.error(
            "--kafka-uri is required if the environment variable "
            f"{KAFKA_URI_ENV_VAR} is not defined."
        )

    return parsed_args


def main():
    args = parse_args()

    logger.info("Loading websites configuration")
    sites = get_sites(args.sites_list)

    logger.info("Initializing Kafka producer")
    producer = Producer(
        args.kafka_uri,
        args.kafka_topic,
        args.kafka_ca,
        args.kafka_cert,
        args.kafka_key,
    )

    def produce(request_data: dict, stats: dict) -> None:
        logger.info(f"Sending: {request_data}: {stats}")
        producer.send(request_data, stats)

    logger.info("Initializing monitoring")
    monitor = Monitor(sites, produce)

    logger.info("Starting monitoring")
    try:
        asyncio.run(monitor.loop(args.check_interval))
    except KeyboardInterrupt:
        logger.warning("Interrupted")
        producer.close()


if __name__ == "__main__":
    main()
