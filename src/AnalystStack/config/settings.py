"""Uses standard dataclasses to pull from environment variables, avoiding hardcoded secrets"""

import os
from dataclasses import dataclass


@dataclass
class BigQuerySettings:
    """Manages default settings for the BigQuery environment."""

    gcp_project_id: str | None = os.getenv("GCP_PROJECT_ID")
    gbq_project_id: str | None = os.getenv("GBQ_PROJECT_ID")
    credentials_path: str | None = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    location: str = os.getenv("BQ_LOCATION", "US")


@dataclass
class DatabricksSettings:
    """Manages default settings for the Databricks environment."""

    server_hostname: str | None = os.getenv("DATABRICKS_SERVER_HOSTNAME")
    http_path: str | None = os.getenv("DATABRICKS_HTTP_PATH")
    access_token: str | None = os.getenv("DATABRICKS_ACCESS_TOKEN")
    catalog: str | None = os.getenv("DATABRICKS_CATALOG")
    schema: str | None = os.getenv("DATABRICKS_SCHEMA")


@dataclass
class PostgresSettings:
    """Manages default settings for the Databricks environment"""

    host: str | None = os.getenv("POSTGRES_HOST")
    port: str | None = os.getenv("POSTGRES_PORT")
    database: str | None = os.getenv("POSTGRES_DATABASE")
    user: str | None = os.getenv("POSTGRES_USER")
    password: str | None = os.getenv("POSTGRES_PASSWORD")
