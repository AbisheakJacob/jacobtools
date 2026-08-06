"""Reshape DataFrames between tidy (long) and normal (wide) layouts."""

from collections.abc import Callable

import pandas as pd


def to_tidy(
    df: pd.DataFrame,
    id_vars: str | list[str],
    value_vars: str | list[str] | None = None,
    var_name: str = "variable",
    value_name: str = "value",
    dropna: bool = True,
) -> pd.DataFrame:
    """
    Reshapes a wide DataFrame into tidy (long) format: one row per observation.

    Args:
        df: The wide-format DataFrame to reshape.
        id_vars: Column(s) that identify each observation and are kept as-is.
        value_vars: Column(s) to unpivot. Defaults to every column not in ``id_vars``.
        var_name: Name of the new column holding the former column labels.
        value_name: Name of the new column holding the former cell values.
        dropna: If True (default), drop rows where ``value_name`` is NaN.

    Returns:
        A tidy DataFrame with columns ``id_vars + [var_name, value_name]``.
    """
    tidy_df = df.melt(id_vars=id_vars, value_vars=value_vars, var_name=var_name, value_name=value_name)
    if dropna:
        tidy_df = tidy_df.dropna(subset=[value_name]).reset_index(drop=True)
    return tidy_df


def from_tidy(
    df: pd.DataFrame,
    index: str | list[str],
    columns: str,
    values: str,
    aggfunc: str | Callable = "first",
    fill_value=None,
) -> pd.DataFrame:
    """
    Reshapes a tidy (long) DataFrame back into normal (wide) format — the inverse of ``to_tidy``.

    Args:
        df: The tidy-format DataFrame to reshape.
        index: Column(s) that identify each row of the wide result.
        columns: Column whose distinct values become new wide columns.
        values: Column holding the values to place into the new wide columns.
        aggfunc: Aggregation applied when multiple rows share the same (index, columns) pair.
        fill_value: Value used to fill any resulting gaps.

    Returns:
        A wide DataFrame with one row per distinct ``index`` value.
    """
    wide_df = df.pivot_table(index=index, columns=columns, values=values, aggfunc=aggfunc, fill_value=fill_value)
    wide_df = wide_df.reset_index()
    wide_df.columns.name = None
    return wide_df
