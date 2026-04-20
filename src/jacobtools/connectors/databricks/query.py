"""Execute SQL in Databricks: Read and Write data"""

import pandas as pd

from Jacobtools.connectors.databricks.client import DatabricksClientWrapper
from Jacobtools.exceptions.errors import QueryExecutionError
from Jacobtools.utils.logging import get_logger

logger = get_logger(__name__)


class QueryManager:
    """Handles read and write data operations to Databricks."""

    def __init__(self, client_wrapper: DatabricksClientWrapper):
        self.wrapper = client_wrapper

    def execute_read(self, query: str) -> pd.DataFrame:
        try:
            logger.debug(f"Executing read query: {query[:100]}...")
            with self._wrapper.client.cursor() as cursor:
                return cursor.execute(query).fetchall_arrow().to_pandas()
        except Exception as e:
            raise QueryExecutionError(f"Query execution failed: {e}")

    def execute_write(
        self, df: pd.DataFrame, catalog: str, schema: str, table_id: str, if_exists: str = "append"
    ) -> None:
        table_ref = f"{catalog}.{schema}.{table_id}"

        try:
            logger.info(f"Writing {len(df)} rows to {table_ref} {if_exists}")

            with self.wrapper.client.cursor() as cursor:

                if if_exists == "replace":
                    cursor.execute(f"DROP TABLE IF EXISTS {table_ref}")

                cursor.write_pandas(df, table_ref, mode="over")

        except Exception as e:
            raise QueryExecutionError(f"Query Execution failed: {e}")
