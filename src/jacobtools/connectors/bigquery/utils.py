"""Any BQ specific text parsing or helper functions"""


def construct_full_table_id(project_id: str, dataset_id: str, table_id: str) -> str:
    """Safely constructs a standard BigQuery standard SQL table reference."""
    return f"`{project_id}.{dataset_id}.{table_id}`"
