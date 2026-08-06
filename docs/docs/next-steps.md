---
icon: material/map
---

# Roadmap / Next steps

This page tracks where AnalystStack is headed. Items are grouped roughly by priority. It is
intentionally opinionated — the goal is a small, dependable toolkit, not a kitchen sink.

## :material-check-all: Recently done

The repo cleanup pass closed several long-standing gaps:

- [x] **`format` CLI works.** `cli.py` now instantiates `PythonFormatter` / `SQLFormatter`
      directly, handles SQL (file-based) and Python (string-based) input correctly, and
      uses plain-ASCII output so it doesn't crash on Windows consoles.
- [x] **Entry point wired.** `analyststack` is installed as a console script.
- [x] **Package `__init__` populated** with `__version__` and top-level conveniences
      (`io`, `PythonFormatter`, `SQLFormatter`, `tidy`, `compare`, `validate`).
- [x] **Real runtime dependencies declared** in `setup.cfg`, with optional extras
      (`bigquery`, `postgres`, `databricks`, `dev`); the spurious `typer` dependency was removed.
- [x] **`SQLFormatter` config fixed** to pass a flat SQLFluff overrides mapping.
- [x] **All connectors run on SQLAlchemy.** BigQuery, Postgres and Databricks each build a
      SQLAlchemy `Engine` and read/write through `pandas.read_sql` / `DataFrame.to_sql`,
      instead of driver-specific code paths.
- [x] **Wire up the Databricks connector.** Exported from `connectors/__init__.py`, with a
      working `read_data` / `write_data` / `get_all_table_names` / `get_datatypes` /
      `get_fillrate`, and covered by tests.
- [x] **Connector parity.** BigQuery, Postgres and Databricks now expose the same surface:
      `read_data`, `write_data`, `get_all_table_names`, `get_datatypes`, `get_fillrate`.
- [x] **`tidy` module** — `to_tidy` / `from_tidy` reshape DataFrames between wide and long.
- [x] **`compare` module** — `compare_dataframes` (match-rate / overlap analysis) and
      `summarize` (one-call EDA profile).
- [x] **`validate` module** — declarative `Rule` / `Validator` for attaching checks to a
      DataFrame before writing it out.

## :material-wrench: Correctness & wiring (do next)

- [ ] **Reconcile `SQLFormatter` input.** `SQLFormatter.format_code` / `view_errors` take a
      **file path**, while `PythonFormatter` takes a **code string**. Make the interface
      consistent (accept a string, or accept both) so both formatters feel the same.

## :material-package-variant: Packaging & dependencies

- [ ] **Single source of truth for metadata.** Consider migrating `setup.cfg` metadata into
      `pyproject.toml` `[project]` to consolidate configuration.
- [ ] **Pin a tested dependency set** for reproducible CI (e.g. a lock file or constraints),
      separate from the loose ranges in `install_requires`.

## :material-test-tube: Testing & quality

- [x] Tests now mirror the package (`io`, `format`, `connectors`, `cli`, `tidy`, `compare`,
      `validate`) and the BigQuery project-id mismatch is fixed.
- [x] Every connector (BigQuery, Postgres, Databricks) has its own test module, mocking
      `sqlalchemy.create_engine` so no test needs real credentials or a network call.
- [ ] Add a coverage gate (e.g. `--cov-fail-under=80`) once coverage stabilises.
- [ ] Add tests for `SQLFormatter` and `DataReader.excel` / `DataWriter.excel`.

## :material-chart-box: Analyst features

Carried over and expanded from the original project goals:

- [ ] **Optional Venn diagram** for `compare_dataframes` — a quick visual on top of the
      existing match-rate / overlap numbers.
- [ ] **DuckDB reader** — a lightweight local engine would make examples runnable without
      cloud credentials.
- [ ] **Pandera-style column schemas** — richer coercion / dtype-casting on top of the
      current rule-based `validate` module, for users who want it.

## :material-book-open-variant: Docs & DX

- [ ] Add API reference pages generated from docstrings (e.g. `mkdocstrings`-style).
- [ ] Add runnable examples / a short tutorial notebook.
- [ ] Publish the site to GitHub Pages on every push to `main` (CI is already set up).

---

!!! info "Contributing"

    Picking something up? Open an issue first so we can agree on the shape of the change,
    then send a PR. CI runs formatting, linting, type checks and tests on every push.
