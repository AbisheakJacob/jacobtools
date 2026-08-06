"""The Databricks Engine (Composition Module)

Isolates authentication and API connection logic"""

from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Engine

from AnalystStack.exceptions.errors import ConnectionError
from AnalystStack.utils.logging import get_logger

logger = get_logger(__name__)


class DatabricksClientWrapper:
    """Wraps a SQLAlchemy engine (via the ``databricks-sqlalchemy`` dialect) securely"""

    def __init__(self, server_hostname: str, http_path: str, access_token: str, catalog: str, schema: str):

        self.server_hostname = server_hostname
        self.http_path = http_path
        self.access_token = access_token
        self.catalog = catalog
        self.schema = schema

        try:
            url = URL.create(
                "databricks",
                username="token",
                password=access_token,
                host=server_hostname,
                query={"http_path": http_path, "catalog": catalog, "schema": schema},
            )
            self._engine: Engine = create_engine(url)
            with self._engine.connect():
                pass
            logger.info(f"Databricks client initialized for server hostname {self.server_hostname}")
        except Exception as e:
            logger.error(f"Failed to initialize Databricks client: {e}")
            raise ConnectionError(f"Client initialization failed: {e}") from e

    @property
    def engine(self) -> Engine:
        return self._engine
