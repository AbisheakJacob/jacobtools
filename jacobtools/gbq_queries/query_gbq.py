import pandas as pd
import pandas_gbq
import bigframes.pandas as bpd
from google.cloud import bigquery

"""
AUTHOR: Abisheak Jacob J
LAST MODIFIED: 04-09-2025
TITLE: Run SQL Query in GBQ
DESCRIPTION: Function to connect to GBQ and run SQL Queries
"""
def query_gbq(
        query: str, 
        str_gcp_project_id: str
    ) -> pd.DataFrame:

    """
    Function to connect to GBQ and run SQL Queries

    Args:
        query (str): the query that needs to be run in gbq
        str_gcp_project_id (np.str): GCP project id under which you need to run this query. Big queries will be billed under this project

    Returns:
        pd.DataFrame: the output of the query is returned as a dataframe
    """

    # excecute query in the respective project
    df_table = pandas_gbq.read_gbq(query, project_id=str_gcp_project_id, dialect="standard", use_bqstorage_api=True)

    return df_table