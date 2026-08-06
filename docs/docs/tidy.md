---
icon: material/swap-vertical
---

# Tidy data

The `tidy` module reshapes DataFrames between **wide** (one column per variable) and
**tidy / long** (one row per observation) layouts — the two shapes analysts constantly
convert between when preparing data for plotting, pivoting, or loading into a warehouse.

```python
from AnalystStack import to_tidy, from_tidy
```

| Function | Description |
| -------- | ----------- |
| `to_tidy(df, id_vars, value_vars=None, var_name="variable", value_name="value", dropna=True)` | Wide → tidy (long). |
| `from_tidy(df, index, columns, values, aggfunc="first", fill_value=None)` | Tidy (long) → wide. |

## Wide to tidy

```python
import pandas as pd
from AnalystStack import to_tidy

sales = pd.DataFrame({"id": [1, 2], "jan": [10, 20], "feb": [30, None]})

tidy = to_tidy(sales, id_vars="id", var_name="month", value_name="sales")
#    id month  sales
# 0   1   jan   10.0
# 1   2   jan   20.0
# 2   1   feb   30.0
```

By default, rows where the value is `NaN` are dropped (`id=2, month=feb` above), since a
missing observation usually isn't a row you want in a tidy table. Pass `dropna=False` to
keep it.

Use `value_vars` to unpivot only a subset of columns; everything not listed in `id_vars` or
`value_vars` is left out of the result.

## Tidy to wide

```python
from AnalystStack import from_tidy

wide = from_tidy(tidy, index="id", columns="month", values="sales")
#    id   feb   jan
# 0   1  30.0  10.0
# 1   2   NaN  20.0
```

If more than one row shares the same `(index, columns)` pair, `aggfunc` (default: `"first"`)
controls how they're combined — pass `"sum"`, `"mean"`, or any function `pivot_table` accepts.
`fill_value` fills in any gaps left by combinations that don't exist in the tidy data.

!!! tip "Round-tripping"

    `from_tidy(to_tidy(df, ...), ...)` recovers the original wide DataFrame as long as no
    values were dropped along the way — handy for verifying a reshape didn't lose data.
