"""Compare two DataFrames key-by-key, and generate one-call summary profiles."""

from dataclasses import dataclass

import pandas as pd


@dataclass
class ComparisonResult:
    """The outcome of comparing two DataFrames on a shared key."""

    left_only_columns: list[str]
    right_only_columns: list[str]
    common_columns: list[str]
    left_only_rows: pd.DataFrame
    right_only_rows: pd.DataFrame
    value_differences: pd.DataFrame
    key_match_rate: float
    row_match_rate: float

    @property
    def is_identical(self) -> bool:
        """True if both DataFrames have identical columns, keys, and values."""
        return (
            not self.left_only_columns
            and not self.right_only_columns
            and self.left_only_rows.empty
            and self.right_only_rows.empty
            and self.value_differences.empty
        )


def compare_dataframes(
    left: pd.DataFrame,
    right: pd.DataFrame,
    on: str | list[str],
    suffixes: tuple[str, str] = ("_left", "_right"),
) -> ComparisonResult:
    """
    Compares two DataFrames that share a key, reporting schema drift, unmatched
    rows, and cell-level value differences.

    Args:
        left: The "before" / baseline DataFrame.
        right: The "after" / candidate DataFrame.
        on: Column(s) that uniquely identify a row in both DataFrames.
        suffixes: Suffixes used internally to disambiguate overlapping column names.

    Returns:
        A ``ComparisonResult`` describing every difference found.
    """
    on_cols = [on] if isinstance(on, str) else list(on)

    left_cols = set(left.columns) - set(on_cols)
    right_cols = set(right.columns) - set(on_cols)
    common_cols = sorted(left_cols & right_cols)
    left_only_columns = sorted(left_cols - right_cols)
    right_only_columns = sorted(right_cols - left_cols)

    merged = left.merge(right, on=on_cols, how="outer", suffixes=suffixes, indicator=True)

    left_only_rows = merged.loc[merged["_merge"] == "left_only", on_cols].reset_index(drop=True)
    right_only_rows = merged.loc[merged["_merge"] == "right_only", on_cols].reset_index(drop=True)
    both = merged.loc[merged["_merge"] == "both"].reset_index(drop=True)

    diff_records = []
    row_is_identical = pd.Series(True, index=both.index)
    for col in common_cols:
        left_col, right_col = f"{col}{suffixes[0]}", f"{col}{suffixes[1]}"
        differs = ~(both[left_col] == both[right_col]) & ~(both[left_col].isna() & both[right_col].isna())
        row_is_identical &= ~differs
        if differs.any():
            mismatched = both.loc[differs, on_cols].copy()
            mismatched["column"] = col
            mismatched["left_value"] = both.loc[differs, left_col].values
            mismatched["right_value"] = both.loc[differs, right_col].values
            diff_records.append(mismatched)

    value_differences = (
        pd.concat(diff_records, ignore_index=True)
        if diff_records
        else pd.DataFrame(columns=[*on_cols, "column", "left_value", "right_value"])
    )

    total_keys = len(merged)
    key_match_rate = len(both) / total_keys if total_keys else 1.0
    row_match_rate = row_is_identical.mean() if len(both) else 1.0

    return ComparisonResult(
        left_only_columns=left_only_columns,
        right_only_columns=right_only_columns,
        common_columns=common_cols,
        left_only_rows=left_only_rows,
        right_only_rows=right_only_rows,
        value_differences=value_differences,
        key_match_rate=float(key_match_rate),
        row_match_rate=float(row_match_rate),
    )


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    """
    Produces a one-call EDA profile of a DataFrame: dtype, null counts,
    cardinality, and basic stats per column.

    Args:
        df: The DataFrame to profile.

    Returns:
        A tidy summary DataFrame with one row per column of ``df``.
    """
    n = len(df)
    rows = []
    for col in df.columns:
        series = df[col]
        non_null = int(series.notna().sum())
        row = {
            "column": col,
            "dtype": str(series.dtype),
            "count": non_null,
            "null_count": n - non_null,
            "null_pct": round((n - non_null) / n * 100, 2) if n else 0.0,
            "n_unique": int(series.nunique(dropna=True)),
            "mean": None,
            "std": None,
            "min": None,
            "max": None,
            "top_value": None,
        }
        if pd.api.types.is_numeric_dtype(series):
            row["mean"] = series.mean()
            row["std"] = series.std()
            row["min"] = series.min()
            row["max"] = series.max()
        else:
            mode = series.mode(dropna=True)
            row["top_value"] = mode.iloc[0] if not mode.empty else None
        rows.append(row)

    return pd.DataFrame(rows)
