import os
from pathlib import Path

import pandas as pd
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from AnalystStack.io.utils import parse_excel_cell
from AnalystStack.utils.logging import get_logger

logger = get_logger(__name__)


class DataReader:
    """Handles comprehensive data ingestion into DataFrames."""

    def excel(
        self,
        file_path: str,
        sheet_name: str | int = 0,
        start_cell: str = "A1",
        end_cell: str | None = None,
        has_header: bool = True,
        **kwargs,
    ) -> pd.DataFrame:
        """
        Reads a specific range of an Excel sheet into a DataFrame.
        """
        logger.info(f"Reading Excel: {file_path} (Sheet: {sheet_name})")

        start_row, _, start_col_letter = parse_excel_cell(start_cell)

        usecols = None
        nrows = None

        if end_cell:
            end_row, _, end_col_letter = parse_excel_cell(end_cell)
            usecols = f"{start_col_letter}:{end_col_letter}"
            # Calculate rows to read (accounting for the header if it exists)
            nrows = (end_row - start_row) if has_header else (end_row - start_row + 1)
        else:
            usecols = f"{start_col_letter}:XFD"  # XFD is the max Excel column

        try:
            df = pd.read_excel(
                file_path,
                sheet_name=sheet_name,
                skiprows=start_row,
                usecols=usecols,
                nrows=nrows,
                header=0 if has_header else None,
                **kwargs,
            )
            return df
        except Exception as e:
            logger.error(f"Failed to read Excel file: {e}")
            raise

    def csv(
        self, file_path: str, skip_rows: int = 0, delimiter: str = ",", has_header: bool = True, **kwargs
    ) -> pd.DataFrame:
        """Reads a CSV file with advanced parsing options."""
        logger.info(f"Reading CSV: {file_path}")
        return pd.read_csv(file_path, skiprows=skip_rows, sep=delimiter, header=0 if has_header else None, **kwargs)

    def parquet(self, file_path: str, columns: list[str] | None = None, **kwargs) -> pd.DataFrame:
        """Reads Parquet files natively."""
        logger.info(f"Reading Parquet: {file_path}")
        return pd.read_parquet(file_path, columns=columns, **kwargs)

    def jinja(self, source: str, **context) -> str:
        """Render a Jinja2 template and return the resulting string.

        ``source`` can be either:

        * a path to a template file, e.g. ``"queries/sales.sql.j2"``, or
        * a raw template string, e.g. ``"SELECT * FROM {{ table }}"``.

        Existing files are loaded from disk (so ``{% include %}`` / ``{% extends %}``
        of sibling templates work); anything else is treated as an inline template
        string. Template variables are supplied as keyword arguments.

        Args:
            source: Path to a template file or an inline template string.
            **context: Variables made available to the template.

        Returns:
            The rendered template as a string.

        Raises:
            jinja2.UndefinedError: If the template references a variable that was
                not supplied (templates are rendered with ``StrictUndefined``).
        """
        if os.path.isfile(source):
            path = Path(source)
            logger.info(f"Rendering Jinja template file: {source}")
            env = Environment(
                loader=FileSystemLoader(str(path.parent)),
                undefined=StrictUndefined,
                keep_trailing_newline=True,
                autoescape=False,
            )
            template = env.get_template(path.name)
        else:
            logger.info("Rendering Jinja template from inline string.")
            env = Environment(
                undefined=StrictUndefined,
                keep_trailing_newline=True,
                autoescape=False,
            )
            template = env.from_string(source)

        return template.render(**context)
