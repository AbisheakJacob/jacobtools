"""Tests for AnalystStack.compare."""

import pandas as pd
import pytest

from AnalystStack.compare import compare_dataframes, summarize


@pytest.fixture
def left() -> pd.DataFrame:
    return pd.DataFrame({"id": [1, 2, 3], "price": [10, 20, 30], "name": ["a", "b", "c"]})


@pytest.fixture
def right() -> pd.DataFrame:
    return pd.DataFrame({"id": [2, 3, 4], "price": [20, 99, 40], "name": ["b", "c", "d"]})


def test_compare_identical_dataframes_reports_no_differences(left):
    result = compare_dataframes(left, left.copy(), on="id")

    assert result.is_identical
    assert result.left_only_rows.empty
    assert result.right_only_rows.empty
    assert result.value_differences.empty
    assert result.key_match_rate == 1.0
    assert result.row_match_rate == 1.0


def test_compare_flags_unmatched_keys(left, right):
    result = compare_dataframes(left, right, on="id")

    assert result.left_only_rows["id"].tolist() == [1]
    assert result.right_only_rows["id"].tolist() == [4]
    assert result.key_match_rate == pytest.approx(2 / 4)


def test_compare_flags_value_differences(left, right):
    result = compare_dataframes(left, right, on="id")

    diffs = result.value_differences
    assert len(diffs) == 1
    row = diffs.iloc[0]
    assert row["id"] == 3
    assert row["column"] == "price"
    assert row["left_value"] == 30
    assert row["right_value"] == 99
    assert result.row_match_rate == pytest.approx(0.5)


def test_compare_detects_schema_drift(left):
    right = left.copy()
    right["extra_col"] = 1
    right = right.drop(columns=["name"])

    result = compare_dataframes(left, right, on="id")

    assert result.right_only_columns == ["extra_col"]
    assert result.left_only_columns == ["name"]
    assert result.common_columns == ["price"]


def test_summarize_returns_one_row_per_column(left):
    summary = summarize(left)

    assert set(summary["column"]) == {"id", "price", "name"}
    assert len(summary) == 3


def test_summarize_numeric_column_stats(left):
    summary = summarize(left).set_index("column")

    price_row = summary.loc["price"]
    assert price_row["null_count"] == 0
    assert price_row["n_unique"] == 3
    assert price_row["mean"] == 20.0
    assert price_row["min"] == 10
    assert price_row["max"] == 30


def test_summarize_reports_nulls_and_top_value():
    df = pd.DataFrame({"category": ["x", "x", "y", None]})
    summary = summarize(df).set_index("column")

    row = summary.loc["category"]
    assert row["null_count"] == 1
    assert row["null_pct"] == 25.0
    assert row["top_value"] == "x"
