---
icon: material/format-paint
---

# Formatting

The `format` module formats and lints code, so generated SQL and Python come out tidy and
consistent. Two formatters are exposed:

```python
from AnalystStack.format import PythonFormatter, SQLFormatter
```

## Python

`PythonFormatter` wraps [Black](https://black.readthedocs.io/) and a syntax check built on
the standard library `ast` module.

| Method | Description |
| ------ | ----------- |
| `view_errors(code_string)` | Return a list of syntax errors (empty if clean). |
| `format_code(code_string)` | Return the Black-formatted source. |

```python
fmt = PythonFormatter(line_length=100)

errors = fmt.view_errors("def f(:\n  pass")     # ["SyntaxError on line 1, ..."]
clean  = fmt.format_code("x={'a':1,'b':2}")     # "x = {\"a\": 1, \"b\": 2}\n"
```

## SQL

`SQLFormatter` wraps [SQLFluff](https://sqlfluff.com/). It reads from and writes to files,
and supports any SQLFluff dialect and templater.

| Method | Description |
| ------ | ----------- |
| `view_errors(file_path)` | Return SQLFluff lint violations for a file. |
| `format_code(file_path, output_path=None)` | Fix a file in place (or write to `output_path`). |

```python
fmt = SQLFormatter(dialect="bigquery", templater="jinja", config_path=".sqlfluff")

violations = fmt.view_errors("query.sql")
fmt.format_code("query.sql")                    # overwrites in place
fmt.format_code("query.sql", "query.fixed.sql") # writes a copy
```

!!! tip "Project-level rules"

    Pass `config_path` pointing at a `.sqlfluff` file to enforce your project's house
    style. AnalystStack ships one at the repo root as a starting point.

## CLI

A `format` command is also exposed for use in scripts and pre-commit hooks:

```bash
analyststack format python path/to/file.py        # format in place
analyststack format sql    path/to/query.sql --lint  # lint only, non-zero exit on errors
```

!!! note "Status"

    The CLI entry point is being finalised — see the [roadmap](next-steps.md).
