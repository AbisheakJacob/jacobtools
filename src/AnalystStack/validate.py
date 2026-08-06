"""Declarative validation for pandas DataFrames.

Build a list of ``Rule`` objects with the factory functions below, bundle them into a
``Validator``, then call ``.validate()`` for a report or ``.enforce()`` to raise on failure.
"""

import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field

import pandas as pd

from AnalystStack.exceptions.errors import ValidationError


@dataclass
class CheckResult:
    """The outcome of evaluating a single ``Rule`` against a DataFrame."""

    rule: str
    column: str | None
    passed: bool
    failed_count: int
    failed_indices: list


@dataclass
class ValidationReport:
    """The combined outcome of every ``Rule`` a ``Validator`` evaluated."""

    results: list[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(result.passed for result in self.results)

    def failures(self) -> list[CheckResult]:
        return [result for result in self.results if not result.passed]

    def to_frame(self) -> pd.DataFrame:
        """Renders the report as a DataFrame — one row per rule evaluated."""
        return pd.DataFrame(
            [
                {"rule": r.rule, "column": r.column, "passed": r.passed, "failed_count": r.failed_count}
                for r in self.results
            ]
        )


class Rule:
    """A single, reusable validation check. ``check`` returns a boolean Series (True = passes)."""

    def __init__(self, name: str, check: Callable[[pd.DataFrame], pd.Series], column: str | None = None):
        self.name = name
        self.column = column
        self._check = check

    def evaluate(self, df: pd.DataFrame) -> CheckResult:
        passes = self._check(df)
        failed_indices = df.index[~passes].tolist()
        return CheckResult(
            rule=self.name,
            column=self.column,
            passed=not failed_indices,
            failed_count=len(failed_indices),
            failed_indices=failed_indices,
        )


# --- Rule factories ----------------------------------------------------------------------


def not_null(column: str) -> Rule:
    """Fails any row where ``column`` is null."""
    return Rule(f"not_null({column})", lambda df: df[column].notna(), column)


def unique(column: str) -> Rule:
    """Fails every row that shares its ``column`` value with another row."""
    return Rule(f"unique({column})", lambda df: ~df[column].duplicated(keep=False), column)


def in_range(column: str, min_value=None, max_value=None) -> Rule:
    """Fails any row where ``column`` falls outside ``[min_value, max_value]`` (either bound optional)."""

    def check(df: pd.DataFrame) -> pd.Series:
        passes = pd.Series(True, index=df.index)
        if min_value is not None:
            passes &= df[column] >= min_value
        if max_value is not None:
            passes &= df[column] <= max_value
        return passes

    return Rule(f"in_range({column})", check, column)


def is_in(column: str, allowed: Iterable) -> Rule:
    """Fails any row whose ``column`` value is not one of ``allowed``."""
    allowed_set = set(allowed)
    return Rule(f"is_in({column})", lambda df: df[column].isin(allowed_set), column)


def matches_regex(column: str, pattern: str) -> Rule:
    """Fails any row where ``column`` (coerced to string) doesn't match ``pattern`` from the start."""
    compiled = re.compile(pattern)
    return Rule(
        f"matches_regex({column})",
        lambda df: df[column].astype(str).map(lambda value: bool(compiled.match(value))),
        column,
    )


def has_dtype(column: str, dtype) -> Rule:
    """Fails every row (as a whole-column check) if ``column`` isn't of the expected ``dtype``."""
    return Rule(f"has_dtype({column})", lambda df: pd.Series(df[column].dtype == dtype, index=df.index), column)


def custom(name: str, check: Callable[[pd.DataFrame], pd.Series], column: str | None = None) -> Rule:
    """Wraps an arbitrary DataFrame -> boolean Series function as a ``Rule``."""
    return Rule(name, check, column)


class Validator:
    """Bundles ``Rule`` objects together and applies them to a DataFrame in one call."""

    def __init__(self, rules: list[Rule] | None = None):
        self.rules: list[Rule] = list(rules or [])

    def add(self, rule: Rule) -> "Validator":
        """Adds a rule and returns self, so calls can be chained."""
        self.rules.append(rule)
        return self

    def validate(self, df: pd.DataFrame) -> ValidationReport:
        """Evaluates every rule and returns a report — never raises."""
        return ValidationReport(results=[rule.evaluate(df) for rule in self.rules])

    def enforce(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validates ``df`` and raises ``ValidationError`` if any rule fails; returns ``df`` unchanged otherwise."""
        report = self.validate(df)
        failures = report.failures()
        if failures:
            details = "; ".join(f"{f.rule} failed on {f.failed_count} row(s)" for f in failures)
            raise ValidationError(f"DataFrame failed validation: {details}")
        return df
