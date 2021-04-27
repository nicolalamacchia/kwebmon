import unittest
from unittest.mock import patch, Mock

from kwebmon.consumer.storage import (
    PostgresStorage,
    CREATE_TABLE_QUERY_FMT,
    INSERT_QUERY_FMT,
)


class TestStorage(unittest.TestCase):
    @patch("kwebmon.consumer.storage.psycopg2.connect")
    def test_storage_db_connection(self, connect_mock):
        test_uri = "http://test:8000"
        storage = PostgresStorage(test_uri, "test_table")
        storage.close = Mock()

        connect_mock.assert_called_once()
        connect_mock.assert_called_with(test_uri)

    @patch("kwebmon.consumer.storage.psycopg2.connect")
    def test_storage_create_table(self, connect_mock):
        test_uri = "http://test:8000"
        test_table = "test_table"

        storage = PostgresStorage(test_uri, test_table)
        storage.close = Mock()

        connect_mock().cursor().execute.assert_called_once()
        connect_mock().cursor().execute.assert_called_with(
            CREATE_TABLE_QUERY_FMT.format(test_table)
        )

    @patch("kwebmon.consumer.storage.psycopg2.connect")
    def test_storage_insert_data(self, connect_mock):
        test_uri = "http://test:8000"
        test_table = "test_table"

        storage = PostgresStorage(test_uri, test_table)
        storage.close = Mock()

        test_data = {
            "url": "test_url",
            "utc_checked_at": "test_timestamp",
            "validation_pattern": None,
            "content_valid": None,
            "response_time": 3.14,
            "status_code": 200,
            "error": None,
        }

        storage.save(**test_data)

        connect_mock().cursor().execute.assert_called_with(
            INSERT_QUERY_FMT.format(test_table),
            (
                test_data["url"],
                test_data["utc_checked_at"],
                test_data["validation_pattern"],
                test_data["content_valid"],
                test_data["response_time"],
                test_data["status_code"],
                test_data["error"],
            ),
        )


if __name__ == "__main__":
    unittest.main()
