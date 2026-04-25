"""Uses standard dataclasses to pull from environment variables, avoiding hardcoded secrets"""

import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class BigQuerySettings:
    """Manages default settings for the BigQuery environment."""

    gcp_project_id: Optional[str] = os.getenv("GCP_PROJECT_ID")
    gbq_project_id: Optional[str] = os.getenv("GBQ_PROJECT_ID")
    credentials_path: Optional[str] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    location: str = os.getenv("BQ_LOCATION", "US")


@dataclass
class DatabricksSettings:
    """Manages default settings for the Databricks environment."""

    server_hostname: Optional[str] = os.getenv("DATABRICKS_SERVER_HOSTNAME")
    http_path: Optional[str] = os.getenv("DATABRICKS_HTTP_PATH")
    access_token: Optional[str] = os.getenv("DATABRICKS_ACCESS_TOKEN")
