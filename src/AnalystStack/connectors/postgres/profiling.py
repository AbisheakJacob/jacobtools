"""Dedicated to heavy analytical queries like calculating fill rates"""

from AnalystStack.connectors.postgres.metadata import MetadataManager
from AnalystStack.connectors.postgres.query import QueryManager


class ProfileManager:
    """Generates data quality statistics and profiles."""

    def __init__(self, query_manager: QueryManager, metadata_manager: MetadataManager):
        self._query_manager = query_manager
        self._metadata_manager = metadata_manager

    def calculate_fillrate(self, schema: str, table_id: str) -> dict[str, float]:
        columns = self._metadata_manager.fetch_datatypes(schema, table_id).keys()
        if not columns:
            return {}

        selects = [
            f'ROUND((SUM(CASE WHEN "{col}" IS NOT NULL THEN 1 ELSE 0 END) '
            f'/ NULLIF(COUNT(*), 0)::numeric) * 100, 2) AS "{col}"'
            for col in columns
        ]

        sql_select = ",\n".join(selects)
        query = f"SELECT \n{sql_select} \nFROM {schema}.{table_id}"

        df = self._query_manager.execute_read(query)
        return {str(key): float(value) for key, value in df.iloc[0].to_dict().items()} if not df.empty else {}
