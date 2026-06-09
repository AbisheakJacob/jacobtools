"""Tests for AnalystStack.io.writer.DataWriter (csv, markdown, txt)."""

import pytest

from AnalystStack.io.writer import DataWriter


@pytest.fixture
def writer() -> DataWriter:
    return DataWriter()


# ---------------------------------------------------------
# csv
# ---------------------------------------------------------


def test_csv_overwrite_writes_header(writer, sample_dataframe, tmp_path):
    path = tmp_path / "out.csv"
    writer.csv(sample_dataframe, str(path))

    text = path.read_text(encoding="utf-8")
    assert text.splitlines()[0] == "id,name,price"
    # 1 header + 3 data rows
    assert len([line for line in text.splitlines() if line]) == 4


def test_csv_append_does_not_duplicate_header(writer, sample_dataframe, tmp_path):
    path = tmp_path / "out.csv"
    writer.csv(sample_dataframe, str(path), mode="overwrite")
    writer.csv(sample_dataframe, str(path), mode="append")

    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line]
    header_count = sum(1 for line in lines if line.startswith("id,name"))
    assert header_count == 1
    assert len(lines) == 1 + 3 + 3  # one header + two batches of data


# ---------------------------------------------------------
# markdown
# ---------------------------------------------------------


def test_markdown_writes_table_from_dataframe(writer, sample_dataframe, tmp_path):
    path = tmp_path / "table.md"
    writer.markdown(sample_dataframe, str(path))

    content = path.read_text(encoding="utf-8")
    assert "id" in content and "name" in content
    assert "|" in content  # markdown table pipes


def test_markdown_writes_raw_string(writer, tmp_path):
    path = tmp_path / "note.md"
    writer.markdown("# Hello", str(path))
    assert path.read_text(encoding="utf-8").startswith("# Hello")


# ---------------------------------------------------------
# txt
# ---------------------------------------------------------


def test_txt_writes_string(writer, tmp_path):
    path = tmp_path / "log.txt"
    writer.txt("run complete", str(path))
    assert path.read_text(encoding="utf-8").strip() == "run complete"


def test_txt_append_mode(writer, tmp_path):
    path = tmp_path / "log.txt"
    writer.txt("line 1", str(path), mode="overwrite")
    writer.txt("line 2", str(path), mode="append")

    lines = [line for line in path.read_text(encoding="utf-8").splitlines() if line]
    assert lines == ["line 1", "line 2"]
