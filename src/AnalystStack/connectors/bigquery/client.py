"""The Bigquery Engine (Composition Module)

Isolates authentication and API connection logic"""

from sqlalchemy import create_engine
from sqlalchemy.engine import URL, Engine

from AnalystStack.exceptions.errors import ConnectionError
from AnalystStack.utils.logging import get_logger

logger = get_logger(__name__)


class BigQueryClientWrapper:
    """Wraps a SQLAlchemy engine (via the ``sqlalchemy-bigquery`` dialect) securely."""

    def __init__(self, gcp_project_id: str, credentials_path: str | None = None):
        self.gcp_project_id = gcp_project_id
        self.credentials_path = credentials_path
        try:
            url = URL.create(
                "bigquery",
                host=gcp_project_id,
                query={"credentials_path": credentials_path} if credentials_path else {},
            )
            self._engine: Engine = create_engine(url)
            with self._engine.connect():
                pass
            logger.info(f"BigQuery client initialized for project {self.gcp_project_id}")
        except Exception as e:
            logger.error(f"Failed to initialize BigQuery client: {e}")
            raise ConnectionError(f"Client initialization failed: {e}") from e

    @property
    def engine(self) -> Engine:
        return self._engine
