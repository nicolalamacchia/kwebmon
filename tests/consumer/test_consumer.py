import unittest
from unittest.mock import patch, Mock, MagicMock

from kwebmon.consumer.consumer import Consumer, InvalidMessageReceivedError


class TestConsumer(unittest.TestCase):
    @patch("kwebmon.consumer.consumer.KafkaConsumer")
    def test_consumer_invalid_value(self, consumer_mock):
        consumer_mock.return_value = [
            MagicMock(
                key={"url": "https://test", "pattern": "test_pattern"},
                value={"error": "Invalid domain"}
            ),
        ]

        consumer = Consumer(
            "http://test:8000",
            "test-topic",
            "cafile",
            "certfile",
            "keyfile",
            "group-id",
        )
        consumer.close = Mock()

        mock = Mock()

        with self.assertRaisesRegex(
                InvalidMessageReceivedError,
                ("An invalid message value has been received: "
                 "{'error': 'Invalid domain'}")
            ):
            consumer.listen(mock)

    @patch("kwebmon.consumer.consumer.KafkaConsumer")
    def test_consumer_invalid_key(self, consumer_mock):
        consumer_mock.return_value=[
            MagicMock(
                key={"pattern": "test_pattern"},
                value={"error": "Invalid domain", "utc_completed_at": "x"}
            ),
        ]

        consumer = Consumer(
            "http://test:8000",
            "test-topic",
            "cafile",
            "certfile",
            "keyfile",
            "group-id",
        )
        consumer.close = Mock()

        mock = Mock()

        with self.assertRaisesRegex(
                InvalidMessageReceivedError,
                ("An invalid message key has been received: "
                 "{'pattern': 'test_pattern'}")
            ):
            consumer.listen(mock)

    @patch("kwebmon.consumer.consumer.KafkaConsumer")
    def test_consumer_valid_message(self, consumer_mock):
        consumer_mock.return_value=[
            MagicMock(
                key={"url": "http://test", "pattern": "test_pattern"},
                value={"error": "Invalid domain", "utc_completed_at": "x"}
            ),
        ]

        consumer = Consumer(
            "http://test:8000",
            "test-topic",
            "cafile",
            "certfile",
            "keyfile",
            "group-id",
        )
        consumer.close = Mock()

        mock = Mock()

        consumer.listen(mock)

        mock.assert_called_with(
            {
                "url": "http://test",
                "pattern": "test_pattern"
            },
            {
                "error": "Invalid domain",
                "utc_completed_at": "x"
            }
        )


if __name__ == "__main__":
    unittest.main()
