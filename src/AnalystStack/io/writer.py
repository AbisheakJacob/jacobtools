import os
from typing import Any, Union

from openpyxl import load_workbook
import pandas as pd

from AnalystStack.io.utils import parse_excel_cell
from AnalystStack.utils.logging import get_logger

logger = get_logger(__name__)


class DataWriter:
    """Handles exporting DataFrames and text to various formats securely."""

    def excel(
        self,
        df: pd.DataFrame,
        file_path: str,
        sheet_name: str = "Sheet1",
        start_cell: str = "A1",
        # clear_range: Optional[str] = None,
        index: bool = False,
        header: bool = True,
        **kwargs,
    ) -> None:
        """
        Writes a DataFrame to Excel. Can target specific cells and safely overlay
        data without destroying the rest of the sheet.
        """
        start_row, start_col, _ = parse_excel_cell(start_cell)

        # 1. Clear specific cells if requested and file exists
        wb = load_workbook(file_path)
        ws = wb[sheet_name]
        # Delete everything below row 1
        # ws.delete_rows(2, ws.max_row)
        wb.remove(ws)
        ws = wb.create_sheet(sheet_name)

        # Save after clearing
        wb.save(file_path)
        wb.close()

        # 2. Write the DataFrame (Overlay mode preserves existing formatting/data outside our target)
        mode = "a" if os.path.exists(file_path) else "w"
        if_exists = "overlay" if mode == "a" else None

        with pd.ExcelWriter(file_path, engine="openpyxl", mode=mode, if_sheet_exists=if_exists) as writer:
            df.to_excel(
                writer,
                sheet_name=sheet_name,
                startrow=start_row,
                startcol=start_col,
                index=index,
                header=header,
                **kwargs,
            )
        logger.info(f"Successfully wrote data to {file_path} at {start_cell}.")

    def csv(self, df: pd.DataFrame, file_path: str, mode: str = "overwrite", index: bool = False) -> None:
        """Writes to CSV. Prevents duplicating the header row when appending."""
        write_mode = "a" if mode == "append" else "w"

        # Only write the header if we are overwriting, OR if the file doesn't exist yet
        write_header = True if write_mode == "w" or not os.path.exists(file_path) else False

        df.to_csv(file_path, mode=write_mode, index=index, header=write_header)
        logger.info(f"Data {'appended' if write_mode == 'a' else 'written'} to {file_path}.")

    def _format_data(self, data: Union[pd.DataFrame, Any], markdown: bool = False) -> str:
        """Internal helper to convert DF to string/markdown, or leave raw text as string."""
        if isinstance(data, pd.DataFrame):
            return data.to_markdown(index=False) if markdown else data.to_string(index=False)
        return str(data)

    def markdown(self, data: Union[pd.DataFrame, str], file_path: str, mode: str = "overwrite") -> None:
        """Writes DataFrame or raw text to a Markdown file."""
        write_mode = "a" if mode == "append" else "w"
        text_data = self._format_data(data, markdown=True)

        with open(file_path, write_mode, encoding="utf-8") as f:
            f.write(text_data + "\n\n")
        logger.info(f"Markdown written to {file_path}.")

    def txt(self, data: Union[pd.DataFrame, str], file_path: str, mode: str = "overwrite") -> None:
        """Writes DataFrame or raw text to a standard TXT file."""
        write_mode = "a" if mode == "append" else "w"
        text_data = self._format_data(data, markdown=False)

        with open(file_path, write_mode, encoding="utf-8") as f:
            f.write(text_data + "\n")
        logger.info(f"Text written to {file_path}.")

    def clipboard(self, data: Union[pd.DataFrame, str]) -> None:
        """Copies DataFrame or text directly to the OS clipboard."""
        if isinstance(data, pd.DataFrame):
            data.to_clipboard(index=False)
        else:
            # Pandas allows us to hijack its clipboard function for plain strings too
            pd.DataFrame([str(data)]).to_clipboard(index=False, header=False)
        logger.info("Data copied to clipboard.")
