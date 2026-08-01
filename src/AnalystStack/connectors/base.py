"""The Abstract Base

This enforces a strict contract. Any future connector (Snowflake, Postgres, etc.) must implements these methods
"""

from abc import ABC, abstractmethod

import pandas as pd


class BaseConnector(ABC):
    """Abstract Base Class defining the contract for all data connectors."""

    @abstractmethod
    def read_data(self, query: str) -> pd.DataFrame:
        """Executes a query and returns a pandas DataFrame."""

    @abstractmethod
    def write_data(
        self,
        df: pd.DataFrame,
        schema: str,
        table_id: str,
        if_exists: str,
    ) -> None:
        """Writes a DataFrame to the destination system."""

    @abstractmethod
    def get_all_table_names(self, schema: str) -> list[str]:
        """Retrieves a list of all tables in a given database/dataset."""
