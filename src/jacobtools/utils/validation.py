"""Ensures safety before executing costly cloud operations"""

import re
from JacobTools.exceptions.errors import ValidationError


def validate_table_reference(gbq_project_id: str, dataset_id: str, table_id: str) -> None:
    """Validates that dataset and table IDs conform to BigQuery naming standards."""
    pattern = r"^[a-zA-Z0-9_]+$"
    if not re.match(pattern, dataset_id):
        raise ValidationError(f"Invalid dataset ID: {dataset_id}")
    if not re.match(pattern, table_id):
        raise ValidationError(f"Invalid table ID: {table_id}")
