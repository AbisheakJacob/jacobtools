"""Tests for AnalystStack.connectors.GoogleBigQueryConnector.

The native ``google.cloud.bigquery.Client`` is patched so these tests never make a
network call to GCP.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from AnalystStack.connectors import GoogleBigQueryConnector
from AnalystStack.exceptions.errors import ConfigurationError, QueryExecutionError

GCP_PROJECT = "test-gcp-project-123"
GBQ_PROJECT = "test-gbq-project-123"

# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def mock_bq_client():
    """Patches the native BigQuery client used inside the client wrapper."""
    with patch("AnalystStack.connectors.bigquery.client.bigquery.Client") as mock_client:
        client_instance = MagicMock()
        mock_client.return_value = client_instance
        mock_client.from_service_account_json.return_value = client_instance
        yield client_instance


@pytest.fixture
def connector(mock_bq_client):
    """A pre-initialised connector wired to the mocked client."""
    return GoogleBigQueryConnector(gcp_project_id=GCP_PROJECT, gbq_project_id=GBQ_PROJECT)


# ---------------------------------------------------------
# Initialisation
# ---------------------------------------------------------


def test_initialization_missing_project_id(monkeypatch):
    """A missing project id (arg and env) raises ConfigurationError."""
    monkeypatch.delenv("GCP_PROJECT_ID", raising=False)
    empty_settings = SimpleNamespace(gcp_project_id=None, gbq_project_id=None, credentials_path=None)
    with (
        patch("AnalystStack.connectors.bigquery.connector.BigQuerySettings", return_value=empty_settings),
        pytest.raises(ConfigurationError, match="A GCP project_id must be provided"),
    ):
        GoogleBigQueryConnector(gcp_project_id=None)


# ---------------------------------------------------------
# read_data
# ---------------------------------------------------------


def test_read_data_success(connector, mock_bq_client, sample_dataframe):
    mock_query_job = MagicMock()
    mock_query_job.to_dataframe.return_value = sample_dataframe
    mock_bq_client.query.return_value = mock_query_job

    query = "SELECT * FROM fake_table"
    result_df = connector.read_data(query)

    mock_bq_client.query.assert_called_once_with(query)
    pd.testing.assert_frame_equal(result_df, sample_dataframe)


def test_read_data_failure(connector, mock_bq_client):
    mock_bq_client.query.side_effect = Exception("GCP Network Timeout")
    with pytest.raises(QueryExecutionError, match="Query execution failed: GCP Network Timeout"):
        connector.read_data("SELECT * FROM fake_table")


# ---------------------------------------------------------
# write_data
# ---------------------------------------------------------


def test_write_data_uses_gbq_project_in_table_ref(connector, mock_bq_client, sample_dataframe):
    mock_load_job = MagicMock()
    mock_bq_client.load_table_from_dataframe.return_value = mock_load_job

    connector.write_data(df=sample_dataframe, dataset_id="test_dataset", table_id="test_table", if_exists="replace")

    mock_bq_client.load_table_from_dataframe.assert_called_once()
    args, _ = mock_bq_client.load_table_from_dataframe.call_args
    assert args[1] == f"{GBQ_PROJECT}.test_dataset.test_table"
    mock_load_job.result.assert_called_once()


def test_write_data_rejects_invalid_table_reference(connector, sample_dataframe):
    from AnalystStack.exceptions.errors import ValidationError

    with pytest.raises(ValidationError):
        connector.write_data(df=sample_dataframe, dataset_id="bad-dataset!", table_id="t")


# ---------------------------------------------------------
# metadata & profiling
# ---------------------------------------------------------


def test_get_datatypes(connector, mock_bq_client):
    schema_df = pd.DataFrame({"column_name": ["id", "name", "price"], "data_type": ["INT64", "STRING", "FLOAT64"]})
    mock_query_job = MagicMock()
    mock_query_job.to_dataframe.return_value = schema_df
    mock_bq_client.query.return_value = mock_query_job

    result = connector.get_datatypes("test_dataset", "test_table")
    assert result == {"id": "INT64", "name": "STRING", "price": "FLOAT64"}


def test_get_fillrate(connector, mock_bq_client):
    schema_df = pd.DataFrame({"column_name": ["id", "name"], "data_type": ["INT64", "STRING"]})
    fillrate_df = pd.DataFrame({"id": [100.0], "name": [95.5]})

    job1, job2 = MagicMock(), MagicMock()
    job1.to_dataframe.return_value = schema_df
    job2.to_dataframe.return_value = fillrate_df
    mock_bq_client.query.side_effect = [job1, job2]

    result = connector.get_fillrate("test_dataset", "test_table")
    assert result == {"id": 100.0, "name": 95.5}
