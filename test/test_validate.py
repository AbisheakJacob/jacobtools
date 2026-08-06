"""Tests for AnalystStack.validate."""

import pandas as pd
import pytest

from AnalystStack.exceptions.errors import ValidationError
from AnalystStack.validate import Validator, custom, has_dtype, in_range, is_in, matches_regex, not_null, unique


@pytest.fixture
def df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "id": [1, 2, 2, 4],
            "price": [10.0, None, 30.0, -5.0],
            "email": ["a@x.com", "not-an-email", "c@x.com", "d@x.com"],
            "status": ["active", "active", "inactive", "unknown"],
        }
    )


def test_not_null_flags_missing_values(df):
    result = not_null("price").evaluate(df)
    assert not result.passed
    assert result.failed_count == 1
    assert result.failed_indices == [1]


def test_unique_flags_all_duplicates(df):
    result = unique("id").evaluate(df)
    assert not result.passed
    assert result.failed_indices == [1, 2]


def test_in_range_flags_out_of_bounds(df):
    result = in_range("price", min_value=0).evaluate(df)
    assert not result.passed
    # index 1 fails because NaN >= 0 is False; index 3 fails because -5.0 < 0
    assert result.failed_indices == [1, 3]


def test_is_in_flags_unexpected_categories(df):
    result = is_in("status", allowed=["active", "inactive"]).evaluate(df)
    assert not result.passed
    assert result.failed_indices == [3]


def test_matches_regex_flags_malformed_values(df):
    result = matches_regex("email", pattern=r"^[^@]+@[^@]+\.[^@]+$").evaluate(df)
    assert not result.passed
    assert result.failed_indices == [1]


def test_has_dtype_passes_for_matching_dtype(df):
    result = has_dtype("id", dtype="int64").evaluate(df)
    assert result.passed


def test_has_dtype_fails_for_mismatched_dtype(df):
    result = has_dtype("id", dtype="float64").evaluate(df)
    assert not result.passed
    assert result.failed_count == len(df)


def test_custom_rule_wraps_arbitrary_check(df):
    rule = custom("price_is_even_id", lambda frame: frame["id"] % 2 == 0)
    result = rule.evaluate(df)
    assert not result.passed
    assert result.failed_indices == [0]


def test_validator_validate_returns_report_without_raising(df):
    validator = Validator([not_null("price"), unique("id")])
    report = validator.validate(df)

    assert not report.passed
    assert {f.rule for f in report.failures()} == {"not_null(price)", "unique(id)"}
    frame = report.to_frame()
    assert set(frame["rule"]) == {"not_null(price)", "unique(id)"}


def test_validator_enforce_raises_with_details(df):
    validator = Validator([not_null("price"), unique("id")])
    with pytest.raises(ValidationError, match="not_null\\(price\\) failed on 1 row"):
        validator.enforce(df)


def test_validator_enforce_returns_df_on_success():
    clean_df = pd.DataFrame({"id": [1, 2, 3], "price": [10.0, 20.0, 30.0]})
    validator = Validator([not_null("price"), unique("id")])

    result = validator.enforce(clean_df)
    pd.testing.assert_frame_equal(result, clean_df)


def test_validator_add_chains():
    validator = Validator().add(not_null("id")).add(unique("id"))
    assert len(validator.rules) == 2
