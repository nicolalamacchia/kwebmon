import argparse
import asyncio
import logging
import sys

from kwebmon.producer.producer import Producer
from kwebmon.producer.monitoring import Monitor
from kwebmon.producer.utils import get_sites

DEFAULT_KAFKA_TOPIC = "kwebmon"
DEFAULT_CHECK_INTERVAL = 5

logger = logging.getLogger("kwebmon.producer")


def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser()
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
    return parser.parse_args(args)


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
