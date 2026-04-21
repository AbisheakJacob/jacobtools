from typing import List, Optional, Union

import pandas as pd

from AnalystStack.io.utils import parse_excel_cell
from AnalystStack.utils.logging import get_logger

logger = get_logger(__name__)


class DataReader:
    """Handles comprehensive data ingestion into DataFrames."""

    def excel(
        self,
        file_path: str,
        sheet_name: Union[str, int] = 0,
        start_cell: str = "A1",
        end_cell: Optional[str] = None,
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

    def parquet(self, file_path: str, columns: Optional[List[str]] = None, **kwargs) -> pd.DataFrame:
        """Reads Parquet files natively."""
        logger.info(f"Reading Parquet: {file_path}")
        return pd.read_parquet(file_path, columns=columns, **kwargs)
