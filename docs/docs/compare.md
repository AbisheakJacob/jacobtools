---
icon: material/compare-horizontal
---

# Compare & summarize

The `compare` module answers two everyday analyst questions: *"how do these two
DataFrames differ?"* and *"what does this DataFrame look like?"*.

```python
from AnalystStack import compare_dataframes, summarize
```

## Comparing two DataFrames

`compare_dataframes(left, right, on, suffixes=("_left", "_right"))` compares two DataFrames
that share a key column (or columns), and reports schema drift, unmatched rows, and
cell-level value differences.

```python
import pandas as pd
from AnalystStack import compare_dataframes

before = pd.DataFrame({"id": [1, 2, 3], "price": [10, 20, 30], "name": ["a", "b", "c"]})
after = pd.DataFrame({"id": [2, 3, 4], "price": [20, 99, 40], "name": ["b", "c", "d"]})

result = compare_dataframes(before, after, on="id")

result.left_only_rows      # rows only in `before`  -> id 1
result.right_only_rows     # rows only in `after`   -> id 4
result.value_differences   # id=3, column="price", left_value=30, right_value=99
result.key_match_rate      # 0.5  -> fraction of keys present in both frames
result.row_match_rate      # 0.5  -> fraction of matched keys with fully identical rows
result.is_identical        # False
```

| Field | Description |
| ----- | ----------- |
| `left_only_columns` / `right_only_columns` / `common_columns` | Schema drift between the two frames. |
| `left_only_rows` / `right_only_rows` | Keys present in only one side. |
| `value_differences` | Long-format table: one row per `(key, column)` that differs. |
| `key_match_rate` | Share of the union of keys present on both sides. |
| `row_match_rate` | Share of matched keys whose rows are fully identical across common columns. |
| `is_identical` | `True` only if there is no schema drift, no unmatched keys, and no value differences. |

## Summarizing a single DataFrame

`summarize(df)` profiles every column in one call — dtype, null counts, cardinality, and
basic stats — as a tidy DataFrame you can eyeball or write straight to a report.

```python
from AnalystStack import summarize

summarize(before)
#   column  dtype  count  null_count  null_pct  n_unique  mean   std   min   max top_value
# 0     id  int64      3           0       0.0         3   2.0   1.0   1.0   3.0      None
# 1  price  int64      3           0       0.0         3  20.0  10.0  10.0  30.0      None
# 2   name    str      3           0       0.0         3  None  None  None  None         a
```

Numeric columns get `mean` / `std` / `min` / `max`; everything else gets `top_value` (the
most frequent non-null value) instead.
