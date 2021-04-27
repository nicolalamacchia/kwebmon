import json

from kafka import KafkaProducer


class Producer:
    """
    Wrapper around KafkaProducer.
    """

    def __init__(
        self,
        connection_uri: str,
        topic: str,
        cafile: str,
        certfile: str,
        keyfile: str,
    ) -> None:
        self._kafka_producer = KafkaProducer(
            key_serializer=lambda k: json.dumps(k).encode("utf-8"),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            bootstrap_servers=connection_uri,
            security_protocol="SSL",
            ssl_cafile=cafile,
            ssl_certfile=certfile,
            ssl_keyfile=keyfile,
        )
        self._topic = topic

    def __del__(self):
        if self._kafka_producer:
            self.close()

    def send(self, key: dict, value: dict) -> None:
        """
        Sends a JSON message to the Kafka topic.

        :param message: the message to be sent
        """

        self._kafka_producer.send(self._topic, key=key, value=value)
        self._kafka_producer.flush()

    def close(self) -> None:
        """
        Closes the Kafka producer.
        """
        self._kafka_producer.flush()
        self._kafka_producer.close()
