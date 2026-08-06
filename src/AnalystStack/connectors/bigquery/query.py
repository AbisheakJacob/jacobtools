"""Dedicated to executing SQL and moving data"""

import pandas as pd
from google.cloud import bigquery

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
            return self.wrapper.client.query(query).to_dataframe()
        except QueryExecutionError as e:
            logger.error(f"Query execution failed: {e}")
            raise

    def execute_write(
        self,
        df: pd.DataFrame,
        schema: str,
        table_id: str,
        if_exists: str = "append",
    ) -> None:
        table_ref = f"{self.gbq_project_id}.{schema}.{table_id}"

        write_disp = (
            bigquery.WriteDisposition.WRITE_TRUNCATE
            if if_exists == "replace"
            else bigquery.WriteDisposition.WRITE_APPEND
        )

        job_config = bigquery.LoadJobConfig(write_disposition=write_disp)

        try:
            logger.info(f"Writing {len(df)} rows to {table_ref} ({if_exists})...")
            job = self.wrapper.client.load_table_from_dataframe(df, table_ref, job_config=job_config)
            job.result()
            logger.info(f"Write complete for {table_ref}.")
        except QueryExecutionError as e:
            logger.error(f"Failed to write DataFrame to {table_ref}: {e}")
            raise
