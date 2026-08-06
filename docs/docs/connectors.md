---
icon: material/database
---

# Connectors

The `connectors` module provides a uniform way to read, write and profile tables in cloud
data warehouses. Each connector implements the `BaseConnector` contract and exposes a few
warehouse-specific extras.

Under the hood, every connector reads and writes through a [SQLAlchemy](https://www.sqlalchemy.org/)
`Engine` (via `pandas.read_sql` / `DataFrame.to_sql`), using the dialect appropriate for the
warehouse: [`sqlalchemy-bigquery`](https://github.com/googleapis/python-bigquery-sqlalchemy)
for BigQuery, the built-in `psycopg2` driver for Postgres, and
[`databricks-sqlalchemy`](https://github.com/databricks/databricks-sqlalchemy) for Databricks.
This keeps the read/write code path identical across warehouses — only the connection URL
and dialect differ.

| Method | Description |
| ------ | ----------- |
| `read_data(query)` | Run a SQL query and return a `pandas.DataFrame`. |
| `write_data(df, dataset_id, table_id, if_exists="append")` | Write a DataFrame to a table. |
| `get_all_table_names(dataset_id)` | List every table in a dataset / schema. |
| `get_datatypes(dataset_id, table_id)` | Return `{column: data_type}` for a table. |
| `get_fillrate(dataset_id, table_id)` | Return `{column: % non-null}` for a table. |

## Google BigQuery

```python
from AnalystStack.connectors import GoogleBigQueryConnector

bq = GoogleBigQueryConnector(
    gcp_project_id="my-gcp-project",     # billing / client project
    gbq_project_id="my-data-project",    # project the data lives in (optional)
    credentials_path="service-account.json",  # optional; uses ADC otherwise
)

df = bq.read_data("SELECT * FROM analytics.orders LIMIT 1000")
bq.write_data(df, dataset_id="analytics", table_id="orders_copy", if_exists="replace")

print(bq.get_datatypes("analytics", "orders"))
print(bq.get_fillrate("analytics", "orders"))
```

### Configuration

Any argument left as `None` falls back to an environment variable:

| Argument | Environment variable |
| -------- | -------------------- |
| `gcp_project_id` | `GCP_PROJECT_ID` |
| `gbq_project_id` | `GBQ_PROJECT_ID` |
| `credentials_path` | `GOOGLE_APPLICATION_CREDENTIALS` |

!!! warning "A project id is required"

    If neither `gcp_project_id` nor `GCP_PROJECT_ID` is set, the connector raises a
    `ConfigurationError`.

## Postgres

```python
from AnalystStack.connectors import PostgresConnector

pg = PostgresConnector(
    host="localhost",
    port="5432",
    database="analytics",
    user="analyst",
    password="secret",
)

df = pg.read_data("SELECT * FROM public.orders LIMIT 1000")
pg.write_data(df, schema="public", table_id="orders_copy", if_exists="replace")

print(pg.get_datatypes("public", "orders"))
print(pg.get_fillrate("public", "orders"))
```

### Configuration

Any argument left as `None` falls back to an environment variable:

| Argument | Environment variable |
| -------- | -------------------- |
| `host` | `POSTGRES_HOST` |
| `port` | `POSTGRES_PORT` |
| `database` | `POSTGRES_DATABASE` |
| `user` | `POSTGRES_USER` |
| `password` | `POSTGRES_PASSWORD` |

## Databricks

```python
from AnalystStack.connectors import DatabricksConnector

db = DatabricksConnector(
    server_hostname="my-workspace.cloud.databricks.com",
    http_path="/sql/1.0/warehouses/abc123",
    access_token="dapi...",
    catalog="main",
    schema="analytics",
)

df = db.read_data("SELECT * FROM orders LIMIT 1000")
db.write_data(df, schema="analytics", table_id="orders_copy", if_exists="replace")

print(db.get_datatypes("analytics", "orders"))
print(db.get_fillrate("analytics", "orders"))
```

### Configuration

Any argument left as `None` falls back to an environment variable:

| Argument | Environment variable |
| -------- | -------------------- |
| `server_hostname` | `DATABRICKS_SERVER_HOSTNAME` |
| `http_path` | `DATABRICKS_HTTP_PATH` |
| `access_token` | `DATABRICKS_ACCESS_TOKEN` |
| `catalog` | `DATABRICKS_CATALOG` |
| `schema` | `DATABRICKS_SCHEMA` |

!!! note "Catalog and schema are fixed at connection time"

    The SQLAlchemy Databricks dialect binds a connection to one catalog and schema, so both
    are required at construction time rather than passed per call.

## Errors

All connector failures raise a subclass of `DataPackageError` from
`AnalystStack.exceptions.errors`:

| Exception | Raised when |
| --------- | ----------- |
| `ConfigurationError` | Settings are missing or invalid. |
| `ConnectionError` | Authentication / client init fails. |
| `QueryExecutionError` | A query or write operation fails. |
| `ValidationError` | Input validation fails (e.g. a malformed table reference). |
