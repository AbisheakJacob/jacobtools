"""
Dedicated to schema extration.
We are injecting the QueryManager to not repeat the to_dataframe logic
"""

from JacobTools.connectors.bigquery.query import QueryManager


class MetadataManager:
    """Handles schema and structural metadata extraction"""

    def __init__(self, query_manager: QueryManager):
        self.qurey_manager = query_manager

    def fetch_tables(self, schema: str) -> list[str]:
        return [schema]
