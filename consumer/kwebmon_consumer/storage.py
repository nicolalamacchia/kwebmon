from typing import Optional

import psycopg2

CREATE_TABLE_QUERY_FMT = """
CREATE TABLE IF NOT EXISTS {} (
    id BIGSERIAL PRIMARY KEY,
    utc_checked_at TIMESTAMP NOT NULL,
    url TEXT NOT NULL,
    validation_pattern TEXT,
    content_valid BOOLEAN,
    status_code INTEGER,
    response_time FLOAT,
    error TEXT
);
"""

INSERT_QUERY_FMT = """
INSERT INTO {}
(
    url,
    utc_checked_at,
    validation_pattern,
    content_valid,
    response_time,
    status_code,
    error
)
VALUES (%s, %s, %s, %s, %s, %s, %s);
"""


class PostgresStorage:
    def __init__(self, connection_uri: str, table_name: str):
        self._conn = psycopg2.connect(connection_uri)
        self._table_name = table_name
        self._create_table()

    def close(self):
        self._conn.close()

    def __del__(self):
        self.close()

    def _create_table(self):
        cur = self._conn.cursor()
        cur.execute(CREATE_TABLE_QUERY_FMT.format(self._table_name))
        self._conn.commit()
        cur.close()

    def save(
        self,
        url: str,
        utc_checked_at: str,
        validation_pattern: Optional[str],
        content_valid: Optional[bool],
        response_time: Optional[float],
        status_code: Optional[int],
        error: Optional[str],
    ):
        cur = self._conn.cursor()
        cur.execute(
            INSERT_QUERY_FMT.format(self._table_name),
            (
                url,
                utc_checked_at,
                validation_pattern,
                content_valid,
                response_time,
                status_code,
                error,
            ),
        )
        self._conn.commit()
        cur.close()
