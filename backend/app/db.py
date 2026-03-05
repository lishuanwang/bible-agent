import os
from contextlib import contextmanager
from typing import Any, Iterator

import pymysql
from pymysql.cursors import DictCursor


class DBConfigError(RuntimeError):
    """Raised when required DB config is missing."""


def _db_config() -> dict[str, Any]:
    host = os.getenv("MYSQL_HOST", "").strip()
    port = int(os.getenv("MYSQL_PORT", "3306"))
    user = os.getenv("MYSQL_USER", "").strip()
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "").strip()

    if not host or not user or not database:
        raise DBConfigError("MYSQL_HOST, MYSQL_USER, MYSQL_DATABASE are required")

    return {
        "host": host,
        "port": port,
        "user": user,
        "password": password,
        "database": database,
        "charset": "utf8mb4",
        "cursorclass": DictCursor,
        "autocommit": True,
    }


@contextmanager
def get_connection() -> Iterator[pymysql.connections.Connection]:
    conn = pymysql.connect(**_db_config())
    try:
        yield conn
    finally:
        conn.close()
