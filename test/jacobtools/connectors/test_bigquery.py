from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from JacobTools.connectors import GoogleBigQueryConnector
from JacobTools.exceptions.errors import (ConfigurationError,
                                          QueryExecutionError)

# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def mock_bq_client():
    """
    Patches the native Google Bigquery client inside your client wrapper.
    This prevents the tests from makking read network calls to GCP
    """
    with patch("JacobTools.connectors.bigquery.client.bigquery.Client") as mock_client:

        client_instance = MagicMock()
        mock_client.return_value = client_instance

        mock_client.from_service_account_json.return_value = client_instance
        yield client_instance


@pytest.fixture
def sample_dataframe():
    """Returns a simple pandas DataFrame to use in write/read tests"""
    return pd.DataFrame({"id": [1, 2], "name": ["Sneaker A", "Sneaker B"]})


@pytest.fixture
def connector(mock_bq_client):
    """Provides a pre-initialized GoogleBigQueryConnector for the tests."""
    return GoogleBigQueryConnector(gcp_project_id="test-gcp-project-123", gbq_project_id="test-gbq-project-123")


# ---------------------------------------------------------
# Test Cases
# ---------------------------------------------------------


def test_initialization_missing_project_id():
    """Test that the connector raises an error if no project id is provided or found in env."""
    with patch("JacobTools.config.settings.BigQuerySettings.gcq_project_id", None):
        with pytest.raises(ConfigurationError, match="A GCP project_id must be provided"):
            GoogleBigQueryConnector(gcp_project_id=None)


def test_read_data_success(connector, mock_bq_client, sample_dataframe):
    """Test that read_data successfully returns a DataFrame from a mocked query."""
    # 1. Setup the mock to return our sample DataFrame when .to_dataframe() is called
    mock_query_job = MagicMock()
    mock_query_job.to_dataframe.return_value = sample_dataframe
    mock_bq_client.query.return_value = mock_query_job

    # 2. Execute the method
    query = "SELECT * FROM fake_table"
    result_df = connector.read_data(query)

    # 3. Assertions
    mock_bq_client.query.assert_called_once_with(query)
    pd.testing.assert_frame_equal(result_df, sample_dataframe)


def test_read_data_failure(connector, mock_bq_client):
    """Test that read_data properly raises a custom QueryExecutionError on failure."""
    # Make the query method throw a generic Exception
    mock_bq_client.query.side_effect = Exception("GCP Network Timeout")

    with pytest.raises(QueryExecutionError, match="Query execution failed: GCP Network Timeout"):
        connector.read_data("SELECT * FROM fake_table")


def test_write_data_success(connector, mock_bq_client, sample_dataframe):
    """Test that write_data triggers the correct load_table_from_dataframe method."""
    mock_load_job = MagicMock()
    mock_bq_client.load_table_from_dataframe.return_value = mock_load_job

    connector.write_data(df=sample_dataframe, dataset_id="test_dataset", table_id="test_table", if_exists="replace")

    # Verify the native BQ client was called with the correct table reference
    mock_bq_client.load_table_from_dataframe.assert_called_once()
    args, kwargs = mock_bq_client.load_table_from_dataframe.call_args
    assert args[1] == "test-project-123.test_dataset.test_table"

    # Verify we waited for the job to complete
    mock_load_job.result.assert_called_once()


def test_get_datatypes(connector, mock_bq_client):
    """Test the metadata schema extraction method."""
    # Create a fake response DataFrame representing INFORMATION_SCHEMA.COLUMNS
    mock_schema_df = pd.DataFrame({"column_name": ["id", "name", "price"], "data_type": ["INT64", "STRING", "FLOAT64"]})

    mock_query_job = MagicMock()
    mock_query_job.to_dataframe.return_value = mock_schema_df
    mock_bq_client.query.return_value = mock_query_job

    result = connector.get_datatypes("test_dataset", "test_table")

    assert result == {"id": "INT64", "name": "STRING", "price": "FLOAT64"}


def test_get_fillrate(connector, mock_bq_client):
    """Test the complex dynamic SQL builder for profiling fill rates."""

    # We need to mock TWO queries here:
    # 1. The call to get_datatypes() to get the columns
    # 2. The actual fill rate calculation query

    # Fake response for fetch_datatypes
    schema_df = pd.DataFrame({"column_name": ["id", "name"], "data_type": ["INT64", "STRING"]})

    # Fake response for the fill rate calculation (always a single row)
    fillrate_df = pd.DataFrame({"id": [100.0], "name": [95.5]})

    # Setup the mock query method to return schema_df the first time it is called,
    # and fillrate_df the second time it is called.
    mock_query_job_1 = MagicMock()
    mock_query_job_1.to_dataframe.return_value = schema_df

    mock_query_job_2 = MagicMock()
    mock_query_job_2.to_dataframe.return_value = fillrate_df

    mock_bq_client.query.side_effect = [mock_query_job_1, mock_query_job_2]

    result = connector.get_fillrate("test_dataset", "test_table")

    assert result == {"id": 100.0, "name": 95.5}
