# import libraries
from jacobtools.config import SchemaStructure
import pandas as pd

"""
AUTHOR: Abisheak Jacob J
LAST MODIFIED: 01-08-2025
TITLE: Drop Columns by Schema Document
DESCRIPTION: Drop columns that are not significant in providing any insight into the data using the DropFlag in the schema document
"""


def drop_columns_by_schema(
    df: pd.DataFrame, schema_df: pd.DataFrame, drop_flag_column: int = SchemaStructure.DROP_FLAG
) -> pd.DataFrame:

    # DOCSTRING
    """
    Drop columns that are not significant in providing any insight into the data using the DropFlag in the schema document.

    PARAMETERS
    -------------------
    df: pd.DataFrame
        This is the input DataFrame where columns need to be dropped
    schema_df: pd.DataFrame
        This is the schema DataFrame with the DropFlag
    drop_flag_column: int
        This is a global variable that indicates the column in the schema where the DropFlag is present

    RETURNS
    -------------------
    pd.DataFrame
        Residual DataFrame after the flagged columns are dropped

    RAISES
    --------------------
    ValueError
        If the column is not in the DataFrame or any other errors
    """

    # drop the columns flagged in schema table
    df.drop(
        columns=[
            col
            for col, flag in zip(df.columns.to_list(), schema_df.iloc[:, drop_flag_column])
            if flag
        ],
        inplace=True,
    )

    return df
