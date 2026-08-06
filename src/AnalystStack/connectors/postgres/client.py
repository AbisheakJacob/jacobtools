"""The Postgres Engine (Composition Module)

Isolates authentication and API connection logic"""

from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Engine

from AnalystStack.exceptions.errors import ConnectionError


class PostgresClientWrapper:
    """Wraps a SQLAlchemy engine (via the ``psycopg2`` driver) securely"""

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
            url = URL.create(
                "postgresql+psycopg2",
                username=user,
                password=password,
                host=host,
                port=int(port) if port else None,
                database=database,
            )
            self._engine: Engine = create_engine(url)
            with self._engine.connect():
                pass
            logger.info(f"Postgres client initialized for {self.host}:{self.port} - database: {self.database}")
        except Exception as e:
            logger.error(f"Failed to initialize Postgres client: {e}")
            raise ConnectionError(f"Client initialization failed: {e}") from e

    @property
    def engine(self) -> Engine:
        return self._engine
