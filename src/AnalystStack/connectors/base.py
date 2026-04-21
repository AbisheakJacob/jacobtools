"""The Abstract Base

This enforces a strict contract. Any future connector (Snowflake, Postgres, etc.) must implements these methods
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

import pandas as pd


class BaseConnector(ABC):
    """Abstract Base Class defining the contract for all data connectors."""

    @abstractmethod
    def read_data(self, query: str) -> pd.DataFrame:
        """Executes a query and returns a pandas DataFrame."""
        pass

    @abstractmethod
    def write_data(
        self,
        df: pd.DataFrame,
        dataset_id: str,
        table_id: str,
        if_exists: str,
    ) -> None:
        """Writes a DataFrame to the destination system."""
        pass

    @abstractmethod
    def get_all_table_names(self, dataset_id: str) -> List[str]:
        """Retrieves a list of all tables in a given database/dataset."""
        pass
