"""The Bigquery Engine (Composition Module)

Isolates authentication and API connection logic"""

from typing import Optional
from google.cloud import bigquery
from JacobTools.exceptions.errors import ConnectionError
from JacobTools.utils.logging import get_logger

logger = get_logger(__name__)


class BigQueryClientWrapper:
    """Wraps the native Google BigQuery client securely."""

    def __init__(self, gcp_project_id: str, credentials_path: Optional[str] = None):
        self.gcp_project_id = gcp_project_id
        try:
            if credentials_path:
                self._client = bigquery.Client.from_service_account_json(credentials_path)
            else:
                self._client = bigquery.Client(project=gcp_project_id)
            logger.info(f"BigQuery client initialized for project {self.gcp_project_id}")
        except Exception as e:
            logger.error(f"Failed to initialize BigQuery client: {e}")
            raise ConnectionError(f"Client initialization failed: {e}")

    @property
    def client(self) -> bigquery.Client:
        return self._client
