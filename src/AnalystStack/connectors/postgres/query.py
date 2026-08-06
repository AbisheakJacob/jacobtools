"""Dedicated to executing postgres SQL and moving data"""

import pandas as pd
from loguru import logger

from AnalystStack.connectors.postgres.client import PostgresClientWrapper
from AnalystStack.exceptions.errors import QueryExecutionError


class QueryManager:
    """Handles read and write data operations to Postgres"""

    def __init__(self, client_wrapper: PostgresClientWrapper):
        self.wrapper = client_wrapper

    def execute_read(self, query: str) -> pd.DataFrame:
        try:
            logger.debug(f"Executing read query: {query[:100]}...")
            return pd.read_sql(query, self.wrapper)

        except QueryExecutionError as e:
            logger.error(f"Query execution failed: {e}")
            raise

    def execute_write(self, df: pd.DataFrame, dataset_id: str, table_id: str, if_exists: str = "append") -> None:
        table_ref = f"{dataset_id}.{table_id}"

        if if_exists not in ("append", "replace", "fail"):
            raise ValueError(f"Invalid if_exists value: {if_exists}")

        try:
            logger.info(f"Writing {len(df)} rows to {table_ref} ({if_exists})..")
            df.to_sql(
                name=table_id, con=self.wrapper, schema=dataset_id, if_exists=if_exists, index=False, method="multi"
            )
            logger.success(f"Write complete for {table_ref}.")
        except QueryExecutionError as e:
            logger.error(f"Failed to write Dataframe to {table_ref}: {e}")
