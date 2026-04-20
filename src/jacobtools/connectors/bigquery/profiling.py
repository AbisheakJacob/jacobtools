"""Dedicated to heavy analyticial queries like calculating fill rates"""

from typing import Dict

from JacobTools.connectors.bigquery.metadata import MetadataManager
from JacobTools.connectors.bigquery.query import QueryManager


class ProfilerManager:
    """Generates data quality statistics and profiles."""

    def __init__(self, query_manager: QueryManager, metadata_manager: MetadataManager, gbq_project_id: str):
        self.gbq_project_id = gbq_project_id
        self.query_manager = query_manager
        self.metadata_manager = metadata_manager

    def calculate_fillrate(self, dataset_id: str, table_id: str) -> Dict[str, float]:
        columns = self.metadata_manager.fetch_datatypes(dataset_id, table_id).keys()
        if not columns:
            return {}

        selects = [
            f"ROUND((SUM(CASE WHEN `{col}` IS NOT NULL THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0)) * 100, 2) AS `{col}`"
            for col in columns
        ]

        sql_select = ",\n".join(selects)
        query = f"SELECT \n{sql_select} \nFROM `{self.gbq_project_id}.{dataset_id}.{table_id}`"

        df = self.query_manager.execute_read(query)
        return df.iloc[0].to_dict() if not df.empty else {}
