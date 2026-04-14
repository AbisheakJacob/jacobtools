import pandas as pd
from .query_gbq import query_gbq
import bigframes.pandas as bpd
from google.cloud import bigquery

"""
AUTHOR: Abisheak Jacob J
LAST MODIFIED: 04-09-2025
TITLE: Generate sql code to create a table in postgres
DESCRIPTION: Generate SQL code to automate the process of writing "CREATE TABLE" sql code.
"""


def fillrate_analysis(
    str_gcp_project_id: str,
    str_gbq_project_id: str,
    str_dataset: str,
    bool_check_all_tables: bool = True,
    lst_tables: list = [],
    bool_save_to_csv: bool = False,
) -> pd.DataFrame:
    """
    Calculates the fill rate (non-null value percentage) for columns in specified BigQuery tables.

    Args:
        str_gcp_project_id (str): The GCP project name used for querying BigQuery.
        str_gbq_project_id (str): The project ID where the tables are located.
        str_dataset (str): The dataset name containing the tables.
        bool_check_all_tables (bool): If True, analyze all tables; otherwise, use lst_tables.
        lst_tables (list): List of table names to include in the analysis.
        bool_save_to_csv (bool): If True, save the result DataFrame to a CSV file.
    Returns:
        pd.DataFrame: A DataFrame containing table name, column name, non-null count,
                      null-like count, total count, and fill rate for each column.
    """

    # Get table and column info
    query_columns = f"""
    SELECT table_name, column_name
    FROM `{str_gbq_project_id}.{str_dataset}.INFORMATION_SCHEMA.COLUMNS`
    """

    columns_df = query_gbq(query=query_columns, str_gcp_project_id=str_gcp_project_id)
    tables = columns_df.groupby("table_name")["column_name"].apply(list).to_dict()

    # list of tables to be included in the fill rate calculation
    if bool_check_all_tables:
        lst_included_tables = list(tables.heys())
    else:
        lst_included_tables = lst_tables

    lst_results = []

    # Step 2: Loop over included tables and calculate fill rate using SQL
    for table_name, column_list in tables.items():
        if table_name not in lst_included_tables:
            continue

        full_table_id = f"{str_gbq_project_id}.{str_dataset}.{table_name}"
        print(f" Processing table: {full_table_id}")

        for col in column_list:
            try:
                query_fillrate = f"""
                SELECT
                COUNT(1) AS total_count,
                SUM(CASE WHEN {col} IS NULL OR LOWER(TRIM(CAST({col} AS STRING))) IN ('null', '') THEN 1
                        ELSE 0 END) AS null_like_count,
                ROUND(1 - SUM(CASE WHEN {col} IS NULL OR LOWER(TRIM(CAST({col} AS STRING))) IN ('null', '') THEN 1
                        ELSE 0 END) / COUNT(1), 4) AS fill_rate
                FROM `{full_table_id}`
                """

                df_stats = query_gbq(query=query_fillrate, str_gcp_project_id=str_gcp_project_id)
                stats = df_stats.iloc[0]

                lst_results.append(
                    {
                        "table_name": table_name,
                        "column_name": col,
                        "non_null_count": stats["total_count"] - stats["null_like_count"],
                        "null_like_count": stats["null_like_count"],
                        "total_count": stats["total_count"],
                        "fill_rate": stats["fill_rate"],
                    }
                )

            except Exception as e:
                print(f" Failed for column '{col}' in table '{table_name}': {e}")

    # Format Output
    df_result = pd.DataFrame(lst_results)
    df_result.sort_values(by="fill_rate", inplace=True)
    df_result.columns = [
        "Table Name",
        "Column Name",
        "Non Null Count",
        "Null Like Count",
        "Total Count",
        "Fill Rate",
    ]

    # Save to CSV
    if bool_save_to_csv:
        df_result.to_csv(
            "fill_rate_summary_{}_{}.csv".format(str_gbq_project_id, str_dataset), index=False
        )

    return df_result
