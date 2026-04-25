import re
from typing import Tuple
import typer 

app = typer.Typer()

@app.command()
def parse_excel_cell(cell: str) -> Tuple[int, int, str]:
    """
    Parses an Excel cell reference (e.g., 'C4') into 0-indexed row/col integers
    and returns the column letter.
    Returns: (row_index, col_index, col_letter)
    """
    match = re.match(r"([A-Za-z]+)([0-9]+)", cell.upper())
    if not match:
        raise ValueError(f"Invalid Excel cell reference: {cell}")

    col_letter, row_str = match.groups()
    row_idx = int(row_str) - 1  # 0-indexed

    # Convert Excel column letter to 0-indexed integer (A=0, B=1, Z=25, AA=26)
    col_idx = 0
    for char in col_letter:
        col_idx = col_idx * 26 + (ord(char) - ord("A") + 1)
    col_idx -= 1

    return row_idx, col_idx, col_letter


if __name__ == "__main__":
    app()
