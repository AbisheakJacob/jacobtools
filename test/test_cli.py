"""Tests for the AnalystStack command-line interface."""

import argparse

import pytest

from AnalystStack.cli import handle_format


def _args(language, file, lint=False):
    return argparse.Namespace(language=language, file=file, lint=lint)


def test_cli_format_python_rewrites_file(tmp_path):
    target = tmp_path / "snippet.py"
    target.write_text("x={1:2}\n", encoding="utf-8")

    with pytest.raises(SystemExit) as exc:
        handle_format(_args("python", str(target)))

    assert exc.value.code == 0
    assert target.read_text(encoding="utf-8") == "x = {1: 2}\n"


def test_cli_lint_clean_python_exits_zero(tmp_path):
    target = tmp_path / "clean.py"
    target.write_text("x = 1\n", encoding="utf-8")

    with pytest.raises(SystemExit) as exc:
        handle_format(_args("python", str(target), lint=True))

    assert exc.value.code == 0


def test_cli_lint_broken_python_exits_nonzero(tmp_path):
    target = tmp_path / "broken.py"
    target.write_text("def f(:\n    pass\n", encoding="utf-8")

    with pytest.raises(SystemExit) as exc:
        handle_format(_args("python", str(target), lint=True))

    assert exc.value.code == 1


def test_cli_missing_file_exits_nonzero():
    with pytest.raises(SystemExit) as exc:
        handle_format(_args("python", "does-not-exist.py"))

    assert exc.value.code == 1
