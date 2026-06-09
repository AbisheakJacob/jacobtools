"""Tests for AnalystStack.io.utils.parse_excel_cell."""

import pytest

from AnalystStack.io.utils import parse_excel_cell


@pytest.mark.parametrize(
    "cell, expected",
    [
        ("A1", (0, 0, "A")),
        ("B2", (1, 1, "B")),
        ("C4", (3, 2, "C")),
        ("Z1", (0, 25, "Z")),
        ("AA1", (0, 26, "AA")),
        ("AB10", (9, 27, "AB")),
    ],
)
def test_parse_excel_cell_valid(cell, expected):
    assert parse_excel_cell(cell) == expected


def test_parse_excel_cell_is_case_insensitive():
    assert parse_excel_cell("c4") == parse_excel_cell("C4")


@pytest.mark.parametrize("cell", ["", "1", "1A", "A", "??"])
def test_parse_excel_cell_invalid_raises(cell):
    with pytest.raises(ValueError, match="Invalid Excel cell reference"):
        parse_excel_cell(cell)
