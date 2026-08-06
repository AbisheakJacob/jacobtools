"""Dedicated to executing SQL and moving data"""

import pandas as pd

from AnalystStack.connectors.bigquery.client import BigQueryClientWrapper
from AnalystStack.exceptions.errors import QueryExecutionError
from AnalystStack.utils.logging import get_logger

logger = get_logger(__name__)


class QueryManager:
    """Handles read and write data operations to BigQuery."""

    def __init__(self, client_wrapper: BigQueryClientWrapper, gbq_project_id: str | None = None):
        self.wrapper = client_wrapper
        self.gbq_project_id = gbq_project_id

    def execute_read(self, query: str) -> pd.DataFrame:
        try:
            logger.debug(f"Executing read query: {query[:100]}...")
            return pd.read_sql(query, self.wrapper.engine)
        except Exception as e:
            logger.exception("Query execution failed")
            raise QueryExecutionError(f"Query execution failed: {e}") from e

    def execute_write(
        self,
        df: pd.DataFrame,
        schema: str,
        table_id: str,
        if_exists: str = "append",
    ) -> None:
        table_ref = f"{self.gbq_project_id}.{schema}.{table_id}"

        if if_exists not in ("append", "replace", "fail"):
            raise ValueError(f"Invalid if_exists value: {if_exists}")

        try:
            logger.info(f"Writing {len(df)} rows to {table_ref} ({if_exists})...")
            df.to_sql(name=table_id, con=self.wrapper.engine, schema=schema, if_exists=if_exists, index=False)
            logger.info(f"Write complete for {table_ref}.")
        except Exception as e:
            logger.exception(f"Failed to write DataFrame to {table_ref}")
            raise QueryExecutionError(f"Failed to write DataFrame to {table_ref}: {e}") from e
