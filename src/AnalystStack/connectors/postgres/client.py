"""The Postgres Engine (Composition Module)

Isolates authentication and API connection logic"""

import psycopg2
from loguru import logger
from psycopg2 import OperationalError
from psycopg2.extensions import connection

from AnalystStack.exceptions.errors import ConnectionError


class PostgresClientWrapper:
    """Wraps the native Postgres client securely"""

    def __init__(
        self,
        host: str,
        port: str | None = None,
        database: str | None = None,
        user: str | None = None,
        password: str | None = None,
    ):

        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

        try:
            self._client = psycopg2.connect(
                host=host, port=port, database=database, user=user, password=password
            )
            logger.info(
                f"Postgres client initialized for {self.host}:{self.port} - database: {self.database}"
            )
        except OperationalError as e:
            logger.error(f"Failed to initialize Postgres client: {e}")
            raise ConnectionError(f"Client initialization failed: {e}")

        @property
        def client(self) -> connection:
            return self._client
