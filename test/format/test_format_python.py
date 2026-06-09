"""Tests for AnalystStack.format.python.PythonFormatter."""

import pytest

from AnalystStack.format import PythonFormatter


@pytest.fixture
def formatter() -> PythonFormatter:
    return PythonFormatter(line_length=100)


def test_view_errors_clean_code_returns_empty(formatter):
    assert formatter.view_errors("x = 1\n") == []


def test_view_errors_reports_syntax_error(formatter):
    errors = formatter.view_errors("def f(:\n    pass\n")
    assert len(errors) == 1
    assert "SyntaxError" in errors[0]


def test_format_code_normalises_quotes_and_spacing(formatter):
    formatted = formatter.format_code("x={'a':1,'b':2}")
    assert formatted == 'x = {"a": 1, "b": 2}\n'


def test_format_code_is_idempotent(formatter):
    once = formatter.format_code("y = [1, 2, 3]")
    twice = formatter.format_code(once)
    assert once == twice


def test_format_code_adds_trailing_newline(formatter):
    assert formatter.format_code("z = 1").endswith("\n")
