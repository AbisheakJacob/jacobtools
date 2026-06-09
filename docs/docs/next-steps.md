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
      (`io`, `PythonFormatter`, `SQLFormatter`).
- [x] **Real runtime dependencies declared** in `setup.cfg`, with optional extras
      (`bigquery`, `databricks`, `dev`); the spurious `typer` dependency was removed.
- [x] **`SQLFormatter` config fixed** to pass a flat SQLFluff overrides mapping.

## :material-wrench: Correctness & wiring (do next)

- [ ] **Reconcile `SQLFormatter` input.** `SQLFormatter.format_code` / `view_errors` take a
      **file path**, while `PythonFormatter` takes a **code string**. Make the interface
      consistent (accept a string, or accept both) so both formatters feel the same.
- [ ] **Wire up the Databricks connector.** The `connectors/databricks` package exists but
      isn't exported from `connectors/__init__.py` or covered by tests.

## :material-package-variant: Packaging & dependencies

- [ ] **Single source of truth for metadata.** Consider migrating `setup.cfg` metadata into
      `pyproject.toml` `[project]` to consolidate configuration.
- [ ] **Pin a tested dependency set** for reproducible CI (e.g. a lock file or constraints),
      separate from the loose ranges in `install_requires`.

## :material-test-tube: Testing & quality

- [x] Tests now mirror the package (`io`, `format`, `connectors`, `cli`) and the BigQuery
      project-id mismatch is fixed.
- [ ] Add a coverage gate (e.g. `--cov-fail-under=80`) once coverage stabilises — current
      coverage is ~60%, with the Databricks connector and `format/sql.py` the main gaps.
- [ ] Add tests for `SQLFormatter` and `DataReader.excel` / `DataWriter.excel`.

## :material-chart-box: Analyst features

Carried over and expanded from the original project goals:

- [ ] **`eda` helper** — one call that profiles a DataFrame: shape, dtypes, null counts,
      cardinality, basic stats. Return a tidy summary DataFrame.
- [ ] **Match-rate / overlap analysis** — compare key columns across two DataFrames and
      report match %, plus an optional Venn diagram for quick visualisation.
- [ ] **Connector parity** — bring Databricks to feature parity with BigQuery
      (`read_data`, `write_data`, metadata, fill rate).
- [ ] **Postgres / DuckDB reader** — the IO docs hint at a `postgres` source; a lightweight
      local engine (DuckDB) would make examples runnable without cloud credentials.

## :material-book-open-variant: Docs & DX

- [ ] Add API reference pages generated from docstrings (e.g. `mkdocstrings`-style).
- [ ] Add runnable examples / a short tutorial notebook.
- [ ] Publish the site to GitHub Pages on every push to `main` (CI is already set up).

---

!!! info "Contributing"

    Picking something up? Open an issue first so we can agree on the shape of the change,
    then send a PR. CI runs formatting, linting, type checks and tests on every push.
