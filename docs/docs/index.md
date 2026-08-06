---
icon: lucide/layers
---

# AnalystStack

**AnalystStack** is a Python toolkit of reusable helpers for the work data analysts do
every day: connecting to data warehouses, reading and writing files, rendering SQL from
templates, and formatting code.

It exists to replace the pile of copy-pasted snippets that every analyst accumulates with
a small, tested, `pip install`-able package.

[Get it on PyPI :material-package:](https://pypi.org/project/AnalystStack/){ .md-button .md-button--primary }
[View on GitHub :fontawesome-brands-github:](https://github.com/AbisheakJacob/AnalystStack){ .md-button }

## Installation

=== "PyPI"

    ```bash
    pip install AnalystStack
    ```

=== "From GitHub"

    ```bash
    pip install "git+https://github.com/AbisheakJacob/AnalystStack"
    ```

=== "Editable (local dev)"

    ```bash
    git clone https://github.com/AbisheakJacob/AnalystStack
    cd AnalystStack
    pip install -e ".[dev]"
    ```

## What's inside

<div class="grid cards" markdown>

-   :material-database: **[Connectors](connectors.md)**

    Read, write and profile tables in Google BigQuery, Postgres and Databricks — all backed
    by SQLAlchemy.

-   :material-swap-horizontal: **[IO](io.md)**

    Read/write Excel, CSV, Parquet, Markdown and text — plus a Jinja template renderer.

-   :material-swap-vertical: **[Tidy data](tidy.md)**

    Reshape DataFrames between wide and tidy (long) layouts.

-   :material-compare-horizontal: **[Compare & summarize](compare.md)**

    Diff two DataFrames by key, or profile one in a single call.

-   :material-check-decagram: **[Validation](validate.md)**

    Attach declarative sanity checks to a DataFrame and enforce them before a write.

-   :material-format-paint: **[Formatting](formatting.md)**

    Format and lint Python (Black) and SQL (SQLFluff) from code or the CLI.

-   :material-map: **[Roadmap](next-steps.md)**

    What's planned next, and how the pieces fit together.

</div>

## Quickstart

```python
from AnalystStack.io import io

# Render a SQL query from an inline Jinja template...
query = io.read.jinja("SELECT * FROM {{ table }} WHERE region = '{{ region }}'",
                      table="sales", region="APAC")

# ...or from a template file on disk.
query = io.read.jinja("queries/monthly_sales.sql.j2", month="2026-05")

# Read an Excel range into a DataFrame.
df = io.read.excel("report.xlsx", sheet_name="Data", start_cell="B2", end_cell="F100")

# Write it back out as Markdown.
io.write.markdown(df, "summary.md")
```

```python
from AnalystStack.connectors import GoogleBigQueryConnector

bq = GoogleBigQueryConnector(gcp_project_id="my-project")
df = bq.read_data("SELECT * FROM dataset.table LIMIT 100")
fill = bq.get_fillrate("dataset", "table")   # column completion %
```

```python
from AnalystStack import to_tidy, compare_dataframes, summarize, Validator, not_null

# Reshape wide -> tidy for plotting or loading.
tidy = to_tidy(df, id_vars="id", var_name="month", value_name="sales")

# See what changed between two snapshots of the same table.
diff = compare_dataframes(before, after, on="id")

# One-call EDA profile, and a guard rail before writing back out.
summarize(df)
Validator([not_null("id")]).enforce(df)
```

!!! tip "Configuration via environment variables"

    Connectors fall back to environment variables, so you rarely need to hardcode
    secrets: `GCP_PROJECT_ID`, `GBQ_PROJECT_ID`, and `GOOGLE_APPLICATION_CREDENTIALS`
    for BigQuery.
