"""Tests for AnalystStack.tidy."""

import pandas as pd
import pytest

from AnalystStack.tidy import from_tidy, to_tidy


@pytest.fixture
def wide_df() -> pd.DataFrame:
    return pd.DataFrame({"id": [1, 2], "jan": [10, 20], "feb": [30, None]})


def test_to_tidy_melts_value_columns(wide_df):
    tidy = to_tidy(wide_df, id_vars="id", var_name="month", value_name="sales")

    assert list(tidy.columns) == ["id", "month", "sales"]
    # dropna=True (default) removes the id=2/feb=NaN row
    assert len(tidy) == 3
    assert not tidy["sales"].isna().any()


def test_to_tidy_keeps_na_when_requested(wide_df):
    tidy = to_tidy(wide_df, id_vars="id", var_name="month", value_name="sales", dropna=False)

    assert len(tidy) == 4
    assert tidy["sales"].isna().sum() == 1


def test_to_tidy_respects_value_vars_subset(wide_df):
    tidy = to_tidy(wide_df, id_vars="id", value_vars=["jan"], var_name="month", value_name="sales")

    assert set(tidy["month"]) == {"jan"}
    assert len(tidy) == 2


def test_from_tidy_reverses_to_tidy(wide_df):
    tidy = to_tidy(wide_df, id_vars="id", var_name="month", value_name="sales", dropna=False)
    wide_again = from_tidy(tidy, index="id", columns="month", values="sales")

    expected = wide_df.set_index("id")[["feb", "jan"]].reset_index()
    pd.testing.assert_frame_equal(wide_again, expected, check_dtype=False)


def test_from_tidy_aggregates_duplicates():
    tidy = pd.DataFrame(
        {
            "id": [1, 1, 2],
            "month": ["jan", "jan", "jan"],
            "sales": [10, 20, 30],
        }
    )
    wide = from_tidy(tidy, index="id", columns="month", values="sales", aggfunc="sum")

    assert wide.loc[wide["id"] == 1, "jan"].iloc[0] == 30
    assert wide.loc[wide["id"] == 2, "jan"].iloc[0] == 30


def test_from_tidy_fill_value():
    tidy = pd.DataFrame({"id": [1, 2], "month": ["jan", "feb"], "sales": [10, 20]})
    wide = from_tidy(tidy, index="id", columns="month", values="sales", fill_value=0)

    assert wide.loc[wide["id"] == 1, "feb"].iloc[0] == 0
    assert wide.loc[wide["id"] == 2, "jan"].iloc[0] == 0
