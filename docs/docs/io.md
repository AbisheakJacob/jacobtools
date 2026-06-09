---
icon: material/swap-horizontal
---

# IO

The `io` module wraps common read/write chores behind a single, pre-instantiated facade:

```python
from AnalystStack.io import io

io.read.csv("data.csv")
io.write.markdown(df, "table.md")
```

`io.read` is a `DataReader` and `io.write` is a `DataWriter`.

## Reading

| Method | Description |
| ------ | ----------- |
| `read.excel(file_path, sheet_name=0, start_cell="A1", end_cell=None, has_header=True)` | Read an Excel range into a DataFrame. |
| `read.csv(file_path, skip_rows=0, delimiter=",", has_header=True)` | Read a CSV with parsing options. |
| `read.parquet(file_path, columns=None)` | Read a Parquet file. |
| `read.jinja(source, **context)` | Render a Jinja2 template — see below. |

### Reading an Excel range

`start_cell` / `end_cell` let you grab a sub-range without loading the whole sheet:

```python
df = io.read.excel("report.xlsx", sheet_name="Data",
                   start_cell="B2", end_cell="F100", has_header=True)
```

### Rendering Jinja templates

`read.jinja(source, **context)` takes a **single** `source` argument that can be *either*
a path to a template file *or* a raw template string, which makes it convenient for
building parameterised SQL.

```python
# 1. Inline template string
query = io.read.jinja(
    "SELECT * FROM {{ table }} WHERE dt = '{{ run_date }}'",
    table="sales",
    run_date="2026-05-01",
)

# 2. Template file on disk (relative or absolute path)
query = io.read.jinja("queries/monthly_sales.sql.j2", month="2026-05")
```

If `source` resolves to an existing file it is loaded via a `FileSystemLoader` rooted at
that file's directory, so `{% include %}` and `{% extends %}` of sibling templates work.
Anything else is treated as an inline template string.

!!! note "Undefined variables raise"

    Templates render with `StrictUndefined`, so referencing a variable you didn't pass
    raises `jinja2.UndefinedError` instead of silently producing an empty string — handy
    for catching typos in query parameters. Autoescaping is **off**, which is what you
    want for SQL/text (not HTML).

## Writing

| Method | Description |
| ------ | ----------- |
| `write.excel(df, file_path, sheet_name="Sheet1", start_cell="A1", index=False, header=True)` | Write a DataFrame into an existing workbook. |
| `write.csv(df, file_path, mode="overwrite", index=False)` | Write/append a CSV without duplicating the header. |
| `write.markdown(data, file_path, mode="overwrite")` | Write a DataFrame or string as Markdown. |
| `write.txt(data, file_path, mode="overwrite")` | Write a DataFrame or string as plain text. |
| `write.clipboard(data)` | Copy a DataFrame or string to the OS clipboard. |

```python
io.write.csv(df, "out.csv", mode="append")          # header written only once
io.write.markdown(df, "summary.md")                  # DataFrame -> Markdown table
io.write.txt("Run completed", "log.txt", mode="append")
io.write.clipboard(df)                               # paste straight into a sheet
```

!!! warning "`write.excel` targets an existing workbook"

    `write.excel` opens the file with `openpyxl`, so the workbook must already exist. It
    replaces the target sheet's contents while leaving other sheets intact.
