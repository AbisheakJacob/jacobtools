"""Dedicated to schema extraction. Notice how we 'inject' the QueryManager so we don't repeat the to_dataframe logic"""

from AnalystStack.connectors.postgres.query import QueryManager


class MetadataManager:
    """Handles schema and structural metadata extraction from INFORMATION_SCHEMA"""

    def __init__(self, query_manager: QueryManager):
        self.query_manager = query_manager

    def fetch_tables(self, schema: str) -> list[str]:
        query = f"""
            SELECT table_name
            FROM {schema}.INFORMATION_SCHEMA.TABLES
            WHERE table_type = 'BASE TABLE'
        """
        df = self.query_manager.execute_read(query)
        return df["table_name"].tolist() if not df.empty else []

    def fetch_datatypes(self, schema, table_id) -> dict[str, str]:
        query = f"""
            SELECT column_name, data_type
            FROM `{schema}.INFORMATION_SCHEMA.COLUMNS`
            WHERE table_name = '{table_id}'
        """
        df = self.query_manager.execute_read(query)
        if df.empty:
            return {}
        return dict(zip(df["column_name"], df["data_type"], strict=True))
