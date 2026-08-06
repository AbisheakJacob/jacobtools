---
icon: material/check-decagram
---

# Validation

The `validate` module makes it cheap to attach a handful of sanity checks to a DataFrame —
particularly one you just read from a warehouse or are about to write back to one — without
reaching for a heavyweight schema library.

```python
from AnalystStack import Validator, not_null, unique, in_range, is_in, matches_regex, has_dtype, custom
```

## Rules

Each factory function returns a `Rule` bound to one column (`custom` can also validate
across the whole frame):

| Rule | Fails when… |
| ---- | ----------- |
| `not_null(column)` | the value is null. |
| `unique(column)` | the value is shared with another row. |
| `in_range(column, min_value=None, max_value=None)` | the value falls outside the bounds (either bound optional). |
| `is_in(column, allowed)` | the value isn't one of `allowed`. |
| `matches_regex(column, pattern)` | the value (as a string) doesn't match `pattern` from the start. |
| `has_dtype(column, dtype)` | the column's dtype doesn't equal `dtype` (a whole-column check). |
| `custom(name, check, column=None)` | your own `df -> bool Series` function returns `False`. |

## Putting rules together

```python
from AnalystStack import Validator, not_null, unique, in_range

validator = Validator([
    not_null("price"),
    unique("id"),
    in_range("price", min_value=0),
])

report = validator.validate(df)   # never raises
report.passed                     # False
report.failures()                 # [CheckResult(rule="in_range(price)", ...)]
report.to_frame()                 # one row per rule, as a DataFrame

validator.enforce(df)             # raises ValidationError describing every failed rule
```

`Validator.add(rule)` returns `self`, so rules can be chained: `Validator().add(not_null("id")).add(unique("id"))`.

## Choosing between `validate` and `enforce`

* Use **`validate(df)`** when you want a report to inspect, log, or write to a data-quality
  dashboard — it always returns a `ValidationReport` and never raises.
* Use **`enforce(df)`** as a guard at a pipeline boundary — e.g. right before
  `connector.write_data(...)` — where a failed check should stop execution. It raises
  `AnalystStack.exceptions.errors.ValidationError` with every failing rule listed in the
  message, and otherwise returns `df` unchanged so it can be chained inline:

```python
from AnalystStack.connectors import GoogleBigQueryConnector

bq = GoogleBigQueryConnector(gcp_project_id="my-project")
bq.write_data(validator.enforce(df), schema="analytics", table_id="orders")
```
