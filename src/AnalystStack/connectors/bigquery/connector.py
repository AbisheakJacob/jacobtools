"""The Facade (The Final Connecter)

This is what your end-users will interact with. it inherits from BaseConnectory to fulfill the contract,
but it offloads the actual work to the managers
"""

import pandas as pd

from AnalystStack.config.settings import BigQuerySettings
from AnalystStack.connectors.base import BaseConnector

# Import the specialized managers
from AnalystStack.connectors.bigquery.client import BigQueryClientWrapper
from AnalystStack.connectors.bigquery.metadata import MetadataManager
from AnalystStack.connectors.bigquery.profiling import ProfilerManager
from AnalystStack.connectors.bigquery.query import QueryManager
from AnalystStack.exceptions.errors import ConfigurationError
from AnalystStack.utils.validation import validate_table_reference


class GoogleBigQueryConnector(BaseConnector):
    """
    Expert-level facade combining client, query, metadata, and profiling logic.
    """

    def __init__(
        self,
        gcp_project_id: str | None = None,
        gbq_project_id: str | None = None,
        credentials_path: str | None = None,
    ):
        # Fall back to environment settings if not explicitly provided
        settings = BigQuerySettings()
        self.gcp_project_id = gcp_project_id or settings.gcp_project_id
        self.gbq_project_id = gbq_project_id or settings.gbq_project_id
        self.credentials_path = credentials_path or settings.credentials_path

        if not self.gcp_project_id:
            raise ConfigurationError("A GCP project_id must be provided or set in environment variables.")

        # Initialize the underlying components
        self._client_wrapper = BigQueryClientWrapper(self.gcp_project_id, self.credentials_path)
        self._query_manager = QueryManager(self._client_wrapper, self.gbq_project_id)
        self._metadata_manager = MetadataManager(self._query_manager, self.gbq_project_id)
        self._profiler_manager = ProfilerManager(self._query_manager, self._metadata_manager, self.gbq_project_id)

    # --- Implement BaseConnector Abstract Methods ---

    def read_data(self, query: str) -> pd.DataFrame:
        return self._query_manager.execute_read(query)

    def write_data(
        self,
        df: pd.DataFrame,
        schema: str,
        table_id: str,
        if_exists: str = "append",
    ) -> None:
        validate_table_reference(schema, table_id)
        self._query_manager.execute_write(df, schema, table_id, if_exists)

    def get_all_table_names(self, schema: str) -> list[str]:
        return self._metadata_manager.fetch_tables(schema)

    # --- Expose Specific BigQuery Methods ---

    def get_datatypes(self, schema: str, table_id: str) -> dict[str, str]:
        """Returns BigQuery specific data types for a table."""
        return self._metadata_manager.fetch_datatypes(schema, table_id)

    def get_fillrate(self, schema: str, table_id: str) -> dict[str, float]:
        """Calculates column-level completion percentage."""
        return self._profiler_manager.calculate_fillrate(schema, table_id)
