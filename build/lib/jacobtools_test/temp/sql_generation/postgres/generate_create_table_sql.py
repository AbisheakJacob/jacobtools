# import libraries
import pandas as pd
import numpy as np

"""
AUTHOR: Abisheak Jacob J
LAST MODIFIED: 04-09-2025
TITLE: Generate sql code to create a table in postgres
DESCRIPTION: Generate SQL code to automate the process of writing "CREATE TABLE" sql code.
"""


def infer_pg_type(series: pd.Series) -> str:

    # DOCSTRING
    """
    Infer efficient Postgres data types from pandas series.

    PARAMETERS
    -------------------
    series: pd.Series
        This is a column of the dataframe for which we are generating SQL code.

    RETURNS
    -------------------
    string: str
        Returns a string that contains the data type of the column

    """
    # integer datatype
    if pd.api.types.is_integer_dtype(series):
        min_val, max_val = series.min(), series.max()
        if min_val >= -32768 and max_val <= 32767:
            return "SMALLINT"  # 2 bytes
        elif min_val >= -2147483648 and max_val <= 2147483647:
            return "INTEGER"  # 4 bytes
        else:
            return "BIGINT"  # 8 bytes
    elif pd.api.types.is_float_dtype(series):
        return "DOUBLE PRECISION"  # PostgreSQL's default 8-byte float
    elif pd.api.types.is_bool_dtype(series):
        return "BOOLEAN"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "TIMESTAMP"
    else:
        max_len = series.astype(str).map(len).max()
        if max_len <= 255:
            return f"VARCHAR({max_len + 10})"
        else:
            return "TEXT"


def generate_create_table_sql(csv_file: str, table_name: str = "my_table") -> str:

    # DOCSTRING
    """
    Generate CREATE TABLE sql for postgres

    PARAMETERS
    -------------------
    csv_file: str
        Path to csv file for which table schema is to be created
    table_name: str
        Name of the table in postgres database

    RETURNS
    -------------------
    str
        SQL Code

    RAISES
    --------------------
    ValueError
        If the column is not in the DataFrame or any other errors
    """
    # Load only 100000 rows for type inference
    df = pd.read_csv(csv_file, nrows=10000)

    # infer efficient data type for each column
    column_types = {col: infer_pg_type(df[col].dropna()) for col in df.columns}

    # generate sql code
    sql_lines = [f'DROP TABLE IF EXISTS "{table_name}";\n\nCREATE TABLE "{table_name}" (']

    for col, dtype in column_types.items():
        sql_lines.append(f'    "{col}" {dtype},')

    sql_lines[-1] = sql_lines[-1].rstrip(",")  # remove last comma

    sql_lines.append(");")

    return print("\n".join(sql_lines))
