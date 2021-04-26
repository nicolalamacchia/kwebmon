import json
from typing import Callable, Any

import jsonschema
from kafka import KafkaConsumer

from kwebmon.consumer.json_schemas import (
    MESSAGE_KEY_SCHEMA,
    MESSAGE_VALUE_SCHEMA
)


class InvalidMessageReceivedError(Exception):
    """
    Exception raised when invalid messages are received.
    """


class Consumer:
    """
    Wrapper around KafkaConsumer.
    """

    def __init__(
        self,
        connection_uri: str,
        topic: str,
        cafile: str,
        certfile: str,
        keyfile: str,
        group_id: str,
    ) -> None:
        self._kafka_consumer = KafkaConsumer(
            topic,
            key_deserializer=lambda k: json.loads(k.decode("utf-8")),
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            bootstrap_servers=connection_uri,
            security_protocol="SSL",
            auto_offset_reset="earliest",
            ssl_cafile=cafile,
            ssl_certfile=certfile,
            ssl_keyfile=keyfile,
            group_id=group_id
        )

    def __del__(self):
        self.close()

    def listen(self, callback: Callable[[dict, dict], Any]) -> None:
        """
        Listens for incoming messages to the specified Kafka topic.
        """
        for message in self._kafka_consumer:
            message_key = message.key
            message_value = message.value

            try:
                jsonschema.validate(
                    instance=message_key,
                    schema=MESSAGE_KEY_SCHEMA
                )
            except (
                jsonschema.ValidationError
            ) as validation_error:
                raise InvalidMessageReceivedError(
                    f"An invalid message key has been received: {message_key}"
                ) from validation_error

            try:

                jsonschema.validate(
                    instance=message_value,
                    schema=MESSAGE_VALUE_SCHEMA
                )
            except (
                jsonschema.ValidationError
            ) as validation_error:
                raise InvalidMessageReceivedError(
                    "An invalid message value has been received: "
                    f"{message_value}"
                ) from validation_error

            callback(message_key, message_value)

    def close(self) -> None:
        """
        Closes the Kafka consumer.
        """
        self._kafka_consumer.close()
