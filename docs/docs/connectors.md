---
icon: material/database
---

# Connectors

The `connectors` module provides a uniform way to read, write and profile tables in cloud
data warehouses. Each connector implements the `BaseConnector` contract and exposes a few
warehouse-specific extras.

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

## Databricks

A Databricks connector is scaffolded under `connectors/databricks` and is **not yet wired
into the public API**. Track its progress on the [roadmap](next-steps.md).

## Errors

All connector failures raise a subclass of `DataPackageError` from
`AnalystStack.exceptions.errors`:

| Exception | Raised when |
| --------- | ----------- |
| `ConfigurationError` | Settings are missing or invalid. |
| `ConnectionError` | Authentication / client init fails. |
| `QueryExecutionError` | A query or write operation fails. |
| `ValidationError` | Input validation fails (e.g. a malformed table reference). |
