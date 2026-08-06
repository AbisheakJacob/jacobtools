"""The Facade (The Final Connector)

This is what your end-users will interact with. it inherits from BaseConnector to fulfill the contract,
but it offloads the actual work to the managers
"""

import pandas as pd

from AnalystStack.config.settings import DatabricksSettings
from AnalystStack.connectors.base import BaseConnector
from AnalystStack.connectors.databricks.client import DatabricksClientWrapper
from AnalystStack.connectors.databricks.metadata import MetadataManager
from AnalystStack.connectors.databricks.profiling import ProfilerManager
from AnalystStack.connectors.databricks.query import QueryManager
from AnalystStack.exceptions.errors import ConfigurationError
from AnalystStack.utils.validation import validate_table_reference


class DatabricksConnector(BaseConnector):
    """Expert-level facade combining client, query, metadata, and profiling logic"""

    def __init__(
        self,
        server_hostname: str | None = None,
        http_path: str | None = None,
        access_token: str | None = None,
        catalog: str | None = None,
        schema: str | None = None,
    ):

        settings = DatabricksSettings()
        self.server_hostname = server_hostname or settings.server_hostname
        self.http_path = http_path or settings.http_path
        self.access_token = access_token or settings.access_token
        self.catalog = catalog or settings.catalog
        self.schema = schema or settings.schema

        if (
            not self.server_hostname
            or not self.http_path
            or not self.access_token
            or not self.catalog
            or not self.schema
        ):
            raise ConfigurationError(
                "A Databricks server_hostname, http_path, access_token, catalog, and schema must be "
                "provided or set in env variables."
            )

        # initialize the underlying components
        self._client_wrapper = DatabricksClientWrapper(
            self.server_hostname, self.http_path, self.access_token, self.catalog, self.schema
        )
        self._query_manager = QueryManager(self._client_wrapper)
        self._metadata_manager = MetadataManager(self._query_manager)
        self._profiler_manager = ProfilerManager(self._query_manager, self._metadata_manager)

    def read_data(self, query: str) -> pd.DataFrame:
        return self._query_manager.execute_read(query)

    def write_data(self, df: pd.DataFrame, schema: str, table_id: str, if_exists: str = "append") -> None:
        validate_table_reference(schema, table_id)
        self._query_manager.execute_write(df, schema, table_id, if_exists)

    def get_all_table_names(self, schema: str) -> list[str]:
        return self._metadata_manager.fetch_tables(schema)

    def get_datatypes(self, schema: str, table_id: str) -> dict[str, str]:
        """Returns Databricks specific data types for a table."""
        return self._metadata_manager.fetch_datatypes(schema, table_id)

    def get_fillrate(self, schema: str, table_id: str) -> dict[str, float]:
        """Calculates column-level completion percentage."""
        return self._profiler_manager.calculate_fillrate(schema, table_id)
