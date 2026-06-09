# AnalystStack

[![CI](https://github.com/AbisheakJacob/AnalystStack/actions/workflows/workflow.yml/badge.svg)](https://github.com/AbisheakJacob/AnalystStack/actions/workflows/workflow.yml)
[![PyPI](https://img.shields.io/pypi/v/AnalystStack.svg)](https://pypi.org/project/AnalystStack/)
[![Python](https://img.shields.io/pypi/pyversions/AnalystStack.svg)](https://pypi.org/project/AnalystStack/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-zensical-blue.svg)](https://abisheakjacob.github.io/AnalystStack/)

**AnalystStack** is a Python toolkit of reusable helpers for the work data analysts do every
day: connecting to data warehouses, reading and writing files, rendering SQL from templates,
and formatting code. It replaces the pile of copy-pasted snippets every analyst accumulates
with a small, tested, `pip install`-able package.

📖 **Full documentation:** <https://abisheakjacob.github.io/AnalystStack/>

## Installation

```bash
# From PyPI
pip install AnalystStack

# With the BigQuery connector
pip install "AnalystStack[bigquery]"

# From GitHub
pip install "git+https://github.com/AbisheakJacob/AnalystStack"
```

## Quickstart

```python
from AnalystStack import io

# Render SQL from an inline Jinja template...
query = io.read.jinja("SELECT * FROM {{ table }} WHERE region = '{{ region }}'",
                      table="sales", region="APAC")

# ...or from a template file on disk.
query = io.read.jinja("queries/monthly_sales.sql.j2", month="2026-05")

# Read an Excel range, write it back out as Markdown.
df = io.read.excel("report.xlsx", sheet_name="Data", start_cell="B2", end_cell="F100")
io.write.markdown(df, "summary.md")
```

```python
from AnalystStack.connectors import GoogleBigQueryConnector

bq = GoogleBigQueryConnector(gcp_project_id="my-project")
df = bq.read_data("SELECT * FROM dataset.table LIMIT 100")
fill = bq.get_fillrate("dataset", "table")   # column completion %
```

## Modules

### Connectors

Read, write and profile tables in cloud data warehouses ([docs](https://abisheakjacob.github.io/AnalystStack/connectors/)).

| Method | Description |
| ------ | ----------- |
| `read_data(query)` | Run a query and return a DataFrame. |
| `write_data(df, dataset_id, table_id, if_exists="append")` | Write a DataFrame to a table. |
| `get_all_table_names(dataset_id)` | List tables in a dataset. |
| `get_datatypes(dataset_id, table_id)` | `{column: data_type}` for a table. |
| `get_fillrate(dataset_id, table_id)` | `{column: % non-null}` for a table. |

Google BigQuery is supported today; a Databricks connector is in progress.

### IO

Read and write data, and render Jinja templates ([docs](https://abisheakjacob.github.io/AnalystStack/io/)).

| Method | Description |
| ------ | ----------- |
| `read.excel` / `read.csv` / `read.parquet` | Read files into DataFrames. |
| `read.jinja(source, **context)` | Render a Jinja template from a **file path or string**. |
| `write.excel` / `write.csv` | Write DataFrames to files. |
| `write.markdown` / `write.txt` | Write a DataFrame or string to Markdown / text. |
| `write.clipboard` | Copy a DataFrame or string to the OS clipboard. |

### Formatting

Format and lint code from Python or the CLI ([docs](https://abisheakjacob.github.io/AnalystStack/formatting/)).

| Class | Description |
| ----- | ----------- |
| `PythonFormatter` | Format and syntax-check Python with Black + `ast`. |
| `SQLFormatter` | Format and lint SQL with SQLFluff. |

```bash
# CLI
analyststack format python path/to/file.py          # format in place
analyststack format sql    path/to/query.sql --lint  # lint only
```

## Development

```bash
git clone https://github.com/AbisheakJacob/AnalystStack
cd AnalystStack
pip install -r requirements.txt        # editable install with dev + bigquery extras
```

Common tasks (see the `Makefile`):

| Command | Description |
| ------- | ----------- |
| `make check` | Run format, lint, type-check and tests. |
| `make test` | Run the test suite with coverage. |
| `make format` / `make lint` / `make typecheck` | Individual quality gates. |
| `make build` | Build the sdist and wheel. |
| `make docs` | Build the documentation site. |

The same gates run in CI via [tox](https://tox.wiki/) (`tox -e format,lint,typecheck`,
`tox -e py312,py313`).

## Roadmap

Planned work — and recently closed gaps — live on the
[roadmap](https://abisheakjacob.github.io/AnalystStack/next-steps/).

## License

Released under the [MIT License](LICENSE).
