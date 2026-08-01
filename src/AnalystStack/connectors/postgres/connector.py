"""The Facade (The Final Connector)

This is what your end-users will interact with. it inherits from BaseConnector to fulfill the contract,
but it offloads the actual work to the managers
"""

import pandas as pd

from AnalystStack.config.settings import PostgresSettings
from AnalystStack.connectors.base import BaseConnector
from AnalystStack.connectors.postgres.client import PostgresClientWrapper
from AnalystStack.connectors.postgres.metadata import MetadataManager
from AnalystStack.connectors.postgres.query import QueryManager
from AnalystStack.exceptions.errors import ConfigurationError
from AnalystStack.utils.validation import validate_table_reference


class PostgresConnector(BaseConnector):
    """Expert-level facade combining client, query, metadata, and profiling logic"""

    def __init__(
        self,
        host: str,
        port: str,
        database: str,
        user: str,
        password: str,
    ):
        # fallback to environment settings if not explicitly provided
        settings = PostgresSettings()
        self.host = host or settings.host
        self.port = port or settings.port
        self.database = database or settings.database
        self.user = user or settings.user
        self.password = password or settings.password

        if not self.host or not self.port or not self.database or not self.user or not self.password:
            raise ConfigurationError(
                "A postgres host / port / database / user / password must be provided or set in environment variables"
            )

        # initialize the underlying components
        self._client_wrapper = PostgresClientWrapper(self.host, self.port, self.database, self.user, self.password)
        self._query_manager = QueryManager(self._client_wrapper)
        self._metadata_manager = MetadataManager(self._query_manager)

    def read_data(self, query: str) -> pd.DataFrame:
        return self._query_manager.execute_read(query)

    def write_data(self, df: pd.DataFrame, schema: str, table_id: str, if_exists: str = "append") -> None:
        validate_table_reference(schema, table_id)
        self._query_manager.execute_write(df, schema, table_id, if_exists)

    def get_all_table_names(self, schema: str) -> list[str]:
        return self._metadata_manager.fetch_tables(schema)
