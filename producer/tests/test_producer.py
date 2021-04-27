import unittest
from unittest.mock import patch

from kwebmon_producer.producer import Producer


@patch("kwebmon_producer.producer.KafkaProducer")
class TestProducer(unittest.TestCase):
    def test_producer_send_message(self, mock_kafka_producer):
        producer = Producer(
            "http://test:8000",
            "test-topic",
            "cafile",
            "certfile",
            "keyfile",
        )
        producer.send({"key": "test_key"}, {"value": "test_value"})

        mock_kafka_producer().send.assert_called_with(
            "test-topic",
            key={"key": "test_key"},
            value={"value": "test_value"}
        )
        mock_kafka_producer().flush.assert_called_once()

    def test_producer_close(self, mock_kafka_producer):
        producer = Producer(
            "http://test:8000",
            "test-topic",
            "cafile",
            "certfile",
            "keyfile",
        )
        producer.close()

        mock_kafka_producer().flush.assert_called_once()
        mock_kafka_producer().close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
