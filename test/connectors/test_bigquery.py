"""Tests for AnalystStack.connectors.GoogleBigQueryConnector.

``sqlalchemy.create_engine`` (and ``pandas.read_sql`` / ``DataFrame.to_sql``) are patched so
these tests never make a network call to GCP.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from AnalystStack.connectors import GoogleBigQueryConnector
from AnalystStack.exceptions.errors import ConfigurationError, ConnectionError, QueryExecutionError, ValidationError

GCP_PROJECT = "test-gcp-project-123"
GBQ_PROJECT = "test-gbq-project-123"

# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def mock_engine():
    """Patches ``create_engine`` used inside the client wrapper."""
    with patch("AnalystStack.connectors.bigquery.client.create_engine") as mock_create_engine:
        engine_instance = MagicMock()
        mock_create_engine.return_value = engine_instance
        yield engine_instance


@pytest.fixture
def connector(mock_engine):
    """A pre-initialised connector wired to the mocked engine."""
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


def test_initialization_wraps_engine_errors():
    """A failure while creating/connecting the engine raises ConnectionError."""
    with (
        patch("AnalystStack.connectors.bigquery.client.create_engine", side_effect=RuntimeError("bad credentials")),
        pytest.raises(ConnectionError, match="Client initialization failed"),
    ):
        GoogleBigQueryConnector(gcp_project_id=GCP_PROJECT)


# ---------------------------------------------------------
# read_data
# ---------------------------------------------------------


def test_read_data_success(connector, mock_engine, sample_dataframe):
    query = "SELECT * FROM fake_table"
    with patch("AnalystStack.connectors.bigquery.query.pd.read_sql", return_value=sample_dataframe) as mock_read_sql:
        result_df = connector.read_data(query)

    mock_read_sql.assert_called_once_with(query, mock_engine)
    pd.testing.assert_frame_equal(result_df, sample_dataframe)


def test_read_data_failure(connector, mock_engine):
    with (
        patch("AnalystStack.connectors.bigquery.query.pd.read_sql", side_effect=Exception("GCP Network Timeout")),
        pytest.raises(QueryExecutionError, match="Query execution failed: GCP Network Timeout"),
    ):
        connector.read_data("SELECT * FROM fake_table")


# ---------------------------------------------------------
# write_data
# ---------------------------------------------------------


def test_write_data_uses_engine(connector, mock_engine, sample_dataframe):
    with patch("pandas.DataFrame.to_sql") as mock_to_sql:
        connector.write_data(df=sample_dataframe, schema="test_dataset", table_id="test_table", if_exists="replace")

    mock_to_sql.assert_called_once_with(
        name="test_table", con=mock_engine, schema="test_dataset", if_exists="replace", index=False
    )


def test_write_data_rejects_invalid_table_reference(connector, sample_dataframe):
    with pytest.raises(ValidationError):
        connector.write_data(df=sample_dataframe, schema="bad-dataset!", table_id="t")


def test_write_data_rejects_invalid_if_exists(connector, sample_dataframe):
    with pytest.raises(ValueError, match="Invalid if_exists value"):
        connector.write_data(df=sample_dataframe, schema="test_dataset", table_id="t", if_exists="bogus")


# ---------------------------------------------------------
# metadata & profiling
# ---------------------------------------------------------


def test_get_datatypes(connector, mock_engine):
    schema_df = pd.DataFrame({"column_name": ["id", "name", "price"], "data_type": ["INT64", "STRING", "FLOAT64"]})
    with patch("AnalystStack.connectors.bigquery.query.pd.read_sql", return_value=schema_df):
        result = connector.get_datatypes("test_dataset", "test_table")
    assert result == {"id": "INT64", "name": "STRING", "price": "FLOAT64"}


def test_get_fillrate(connector, mock_engine):
    schema_df = pd.DataFrame({"column_name": ["id", "name"], "data_type": ["INT64", "STRING"]})
    fillrate_df = pd.DataFrame({"id": [100.0], "name": [95.5]})

    with patch("AnalystStack.connectors.bigquery.query.pd.read_sql", side_effect=[schema_df, fillrate_df]):
        result = connector.get_fillrate("test_dataset", "test_table")
    assert result == {"id": 100.0, "name": 95.5}
