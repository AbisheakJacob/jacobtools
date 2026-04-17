"""The Facade (The Final Connecter)

This is what your end-users will interact with. it inherits from BaseConnectory to fulfill the contract, but it offloads the actual work to the managers
"""

from typing import List, Dict, Optional
import pandas as pd

from JacobTools.connectors.base import BaseConnector
from JacobTools.config.settings import BigQuerySettings
from JacobTools.exceptions.errors import ConfigurationError
from JacobTools.utils.validation import validate_table_reference

# Import the specialized managers
from JacobTools.connectors.bigquery.client import BigQueryClientWrapper
from JacobTools.connectors.bigquery.query import QueryManager
from JacobTools.connectors.bigquery.metadata import MetadataManager
from JacobTools.connectors.bigquery.profiling import ProfilerManager


class GoogleBigQueryConnector(BaseConnector):
    """
    Expert-level facade combining client, query, metadata, and profiling logic.
    """

    def __init__(
            self,
            gcp_project_id: Optional[str] = None,
            gbq_project_id: Optional[str] = None,
            credentials_path: Optional[str] = None
    ):
        # Fall back to environment settings if not explicitly provided
        settings = BigQuerySettings()
        self.gcp_project_id = gcp_project_id or settings.gcp_project_id
        self.gbq_project_id = gbq_project_id or settings.gbq_project_id
        self.credentials_path = credentials_path or settings.credentials_path

        if not self.gcp_project_id:
            raise ConfigurationError(
                "A GCP project_id must be provided or set in environment variables."
            )

        # Initialize the underlying components
        self._client_wrapper = BigQueryClientWrapper(self.gcp_project_id, self.credentials_path)
        self._query_manager = QueryManager(self._client_wrapper, self.gbq_project_id)
        self._metadata_manager = MetadataManager(self._client_wrapper, self._query_manager, self.gbq_project_id)
        self._profiler_manager = ProfilerManager(self._query_manager, self._metadata_manager, self.gbq_project_id)

    # --- Implement BaseConnector Abstract Methods ---

    def read_data(self, query: str) -> pd.DataFrame:
        return self._query_manager.execute_read(query)

    def write_data(
        self, df: pd.DataFrame, dataset_id: str, table_id: str, if_exists: str = "append"
    ) -> None:
        validate_table_reference(self.gbq_project_id, dataset_id, table_id)
        self._query_manager.execute_write(df, dataset_id, table_id, if_exists)

    def get_all_table_names(self, dataset_id: str) -> List[str]:
        return self._metadata_manager.fetch_tables(dataset_id)

    # --- Expose Specific BigQuery Methods ---

    def get_datatypes(self, dataset_id: str, table_id: str) -> Dict[str, str]:
        """Returns BigQuery specific data types for a table."""
        return self._metadata_manager.fetch_datatypes(dataset_id, table_id)

    def get_fillrate(self, dataset_id: str, table_id: str) -> Dict[str, float]:
        """Calculates column-level completion percentage."""
        return self._profiler_manager.calculate_fillrate(dataset_id, table_id)
