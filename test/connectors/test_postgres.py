"""Tests for AnalystStack.connectors.PostgresConnector.

``sqlalchemy.create_engine`` (and ``pandas.read_sql`` / ``DataFrame.to_sql``) are patched so
these tests never make a network call to a real Postgres server.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from AnalystStack.connectors import PostgresConnector
from AnalystStack.exceptions.errors import ConfigurationError, ConnectionError, QueryExecutionError, ValidationError

HOST, PORT, DATABASE, USER, PASSWORD = "localhost", "5432", "analytics", "analyst", "secret"

# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def mock_engine():
    """Patches ``create_engine`` used inside the client wrapper."""
    with patch("AnalystStack.connectors.postgres.client.create_engine") as mock_create_engine:
        engine_instance = MagicMock()
        mock_create_engine.return_value = engine_instance
        yield engine_instance


@pytest.fixture
def connector(mock_engine):
    """A pre-initialised connector wired to the mocked engine."""
    return PostgresConnector(host=HOST, port=PORT, database=DATABASE, user=USER, password=PASSWORD)


# ---------------------------------------------------------
# Initialisation
# ---------------------------------------------------------


def test_initialization_missing_settings(monkeypatch):
    """Missing connection settings (args and env) raise ConfigurationError."""
    for var in ("POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_DATABASE", "POSTGRES_USER", "POSTGRES_PASSWORD"):
        monkeypatch.delenv(var, raising=False)
    empty_settings = SimpleNamespace(host=None, port=None, database=None, user=None, password=None)
    with (
        patch("AnalystStack.connectors.postgres.connector.PostgresSettings", return_value=empty_settings),
        pytest.raises(ConfigurationError, match="host / port / database / user / password"),
    ):
        PostgresConnector(host=None, port=None, database=None, user=None, password=None)


def test_initialization_wraps_engine_errors():
    """A failure while creating/connecting the engine raises ConnectionError."""
    with (
        patch("AnalystStack.connectors.postgres.client.create_engine", side_effect=RuntimeError("bad credentials")),
        pytest.raises(ConnectionError, match="Client initialization failed"),
    ):
        PostgresConnector(host=HOST, port=PORT, database=DATABASE, user=USER, password=PASSWORD)


# ---------------------------------------------------------
# read_data
# ---------------------------------------------------------


def test_read_data_success(connector, mock_engine, sample_dataframe):
    query = "SELECT * FROM fake_table"
    with patch("AnalystStack.connectors.postgres.query.pd.read_sql", return_value=sample_dataframe) as mock_read_sql:
        result_df = connector.read_data(query)

    mock_read_sql.assert_called_once_with(query, mock_engine)
    pd.testing.assert_frame_equal(result_df, sample_dataframe)


def test_read_data_failure(connector, mock_engine):
    with (
        patch("AnalystStack.connectors.postgres.query.pd.read_sql", side_effect=Exception("connection reset")),
        pytest.raises(QueryExecutionError, match="Query execution failed: connection reset"),
    ):
        connector.read_data("SELECT * FROM fake_table")


# ---------------------------------------------------------
# write_data
# ---------------------------------------------------------


def test_write_data_uses_engine(connector, mock_engine, sample_dataframe):
    with patch("pandas.DataFrame.to_sql") as mock_to_sql:
        connector.write_data(df=sample_dataframe, schema="public", table_id="products", if_exists="replace")

    mock_to_sql.assert_called_once_with(
        name="products", con=mock_engine, schema="public", if_exists="replace", index=False
    )


def test_write_data_rejects_invalid_table_reference(connector, sample_dataframe):
    with pytest.raises(ValidationError):
        connector.write_data(df=sample_dataframe, schema="bad-schema!", table_id="t")


def test_write_data_rejects_invalid_if_exists(connector, sample_dataframe):
    with pytest.raises(ValueError, match="Invalid if_exists value"):
        connector.write_data(df=sample_dataframe, schema="public", table_id="t", if_exists="bogus")


def test_write_data_wraps_failures(connector, mock_engine, sample_dataframe):
    with (
        patch("pandas.DataFrame.to_sql", side_effect=Exception("disk full")),
        pytest.raises(QueryExecutionError, match="Failed to write DataFrame to public.products: disk full"),
    ):
        connector.write_data(df=sample_dataframe, schema="public", table_id="products")


# ---------------------------------------------------------
# metadata & profiling
# ---------------------------------------------------------


def test_get_all_table_names(connector, mock_engine):
    tables_df = pd.DataFrame({"table_name": ["orders", "customers"]})
    with patch("AnalystStack.connectors.postgres.query.pd.read_sql", return_value=tables_df):
        result = connector.get_all_table_names("public")
    assert result == ["orders", "customers"]


def test_get_datatypes(connector, mock_engine):
    schema_df = pd.DataFrame({"column_name": ["id", "name", "price"], "data_type": ["integer", "text", "numeric"]})
    with patch("AnalystStack.connectors.postgres.query.pd.read_sql", return_value=schema_df):
        result = connector.get_datatypes("public", "products")
    assert result == {"id": "integer", "name": "text", "price": "numeric"}


def test_get_fillrate(connector, mock_engine):
    schema_df = pd.DataFrame({"column_name": ["id", "name"], "data_type": ["integer", "text"]})
    fillrate_df = pd.DataFrame({"id": [100.0], "name": [95.5]})

    with patch("AnalystStack.connectors.postgres.query.pd.read_sql", side_effect=[schema_df, fillrate_df]):
        result = connector.get_fillrate("public", "products")
    assert result == {"id": 100.0, "name": 95.5}
