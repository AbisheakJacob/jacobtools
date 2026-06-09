"""Tests for AnalystStack.io.reader.DataReader (jinja + csv)."""

import pandas as pd
import pytest
from jinja2 import UndefinedError

from AnalystStack.io.reader import DataReader


@pytest.fixture
def reader() -> DataReader:
    return DataReader()


# ---------------------------------------------------------
# jinja: inline template string
# ---------------------------------------------------------


def test_jinja_renders_inline_string(reader):
    result = reader.jinja("SELECT * FROM {{ table }}", table="sales")
    assert result == "SELECT * FROM sales"


def test_jinja_inline_with_multiple_variables(reader):
    template = "SELECT * FROM {{ table }} WHERE region = '{{ region }}'"
    assert reader.jinja(template, table="orders", region="APAC") == ("SELECT * FROM orders WHERE region = 'APAC'")


def test_jinja_supports_control_structures(reader):
    template = "{% for c in cols %}{{ c }}{% if not loop.last %}, {% endif %}{% endfor %}"
    assert reader.jinja(template, cols=["a", "b", "c"]) == "a, b, c"


def test_jinja_missing_variable_raises(reader):
    with pytest.raises(UndefinedError):
        reader.jinja("SELECT * FROM {{ table }}")


# ---------------------------------------------------------
# jinja: template file on disk
# ---------------------------------------------------------


def test_jinja_renders_file(reader, tmp_path):
    template_file = tmp_path / "query.sql.j2"
    template_file.write_text("SELECT * FROM {{ table }} LIMIT {{ n }}", encoding="utf-8")

    result = reader.jinja(str(template_file), table="events", n=10)
    assert result == "SELECT * FROM events LIMIT 10"


def test_jinja_file_supports_includes(reader, tmp_path):
    (tmp_path / "_where.sql.j2").write_text("WHERE dt = '{{ dt }}'", encoding="utf-8")
    main = tmp_path / "main.sql.j2"
    main.write_text("SELECT 1 {% include '_where.sql.j2' %}", encoding="utf-8")

    result = reader.jinja(str(main), dt="2026-05-01")
    assert result == "SELECT 1 WHERE dt = '2026-05-01'"


def test_jinja_string_that_looks_like_path_but_does_not_exist(reader):
    # A non-existent path is treated as an inline template, not a file error.
    result = reader.jinja("queries/{{ name }}.sql", name="x")
    assert result == "queries/x.sql"


# ---------------------------------------------------------
# csv
# ---------------------------------------------------------


def test_csv_roundtrip(reader, tmp_path):
    csv_path = tmp_path / "data.csv"
    pd.DataFrame({"a": [1, 2], "b": ["x", "y"]}).to_csv(csv_path, index=False)

    df = reader.csv(str(csv_path))
    assert list(df.columns) == ["a", "b"]
    assert df.shape == (2, 2)
