"""Dedicated to schema extraction. Notice how we 'inject' the QueryManager so we don't repeat the to_dataframe logic"""

from AnalystStack.connectors.databricks.query import QueryManager


class MetadataManager:
    """Handles schema and structural metadata extraction from INFORMATION_SCHEMA."""

    def __init__(self, query_manager: QueryManager):
        self.query_manager = query_manager

    def fetch_tables(self, schema: str) -> list[str]:
        query = f"""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = '{schema}' AND table_type = 'BASE TABLE'
        """
        df = self.query_manager.execute_read(query)
        return df["table_name"].tolist() if not df.empty else []

    def fetch_datatypes(self, schema: str, table_id: str) -> dict[str, str]:
        query = f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = '{schema}' AND table_name = '{table_id}'
        """
        df = self.query_manager.execute_read(query)
        if df.empty:
            return {}
        return dict(zip(df["column_name"], df["data_type"], strict=True))
