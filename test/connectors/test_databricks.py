"""Tests for AnalystStack.connectors.DatabricksConnector.

``sqlalchemy.create_engine`` (and ``pandas.read_sql`` / ``DataFrame.to_sql``) are patched so
these tests never make a network call to a real Databricks workspace.
"""

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from AnalystStack.connectors import DatabricksConnector
from AnalystStack.exceptions.errors import ConfigurationError, ConnectionError, QueryExecutionError, ValidationError

SERVER_HOSTNAME = "example.cloud.databricks.com"
HTTP_PATH = "/sql/1.0/warehouses/abc123"
ACCESS_TOKEN = "dapi_test_token"
CATALOG = "main"
SCHEMA = "analytics"

# ---------------------------------------------------------
# Fixtures
# ---------------------------------------------------------


@pytest.fixture
def mock_engine():
    """Patches ``create_engine`` used inside the client wrapper."""
    with patch("AnalystStack.connectors.databricks.client.create_engine") as mock_create_engine:
        engine_instance = MagicMock()
        mock_create_engine.return_value = engine_instance
        yield engine_instance


@pytest.fixture
def connector(mock_engine):
    """A pre-initialised connector wired to the mocked engine."""
    return DatabricksConnector(
        server_hostname=SERVER_HOSTNAME,
        http_path=HTTP_PATH,
        access_token=ACCESS_TOKEN,
        catalog=CATALOG,
        schema=SCHEMA,
    )


# ---------------------------------------------------------
# Initialisation
# ---------------------------------------------------------


def test_initialization_missing_settings(monkeypatch):
    """Missing connection settings (args and env) raise ConfigurationError."""
    for var in (
        "DATABRICKS_SERVER_HOSTNAME",
        "DATABRICKS_HTTP_PATH",
        "DATABRICKS_ACCESS_TOKEN",
        "DATABRICKS_CATALOG",
        "DATABRICKS_SCHEMA",
    ):
        monkeypatch.delenv(var, raising=False)
    empty_settings = SimpleNamespace(server_hostname=None, http_path=None, access_token=None, catalog=None, schema=None)
    with (
        patch("AnalystStack.connectors.databricks.connector.DatabricksSettings", return_value=empty_settings),
        pytest.raises(ConfigurationError, match="server_hostname, http_path, access_token, catalog, and schema"),
    ):
        DatabricksConnector()


def test_initialization_wraps_engine_errors():
    """A failure while creating/connecting the engine raises ConnectionError."""
    with (
        patch("AnalystStack.connectors.databricks.client.create_engine", side_effect=RuntimeError("bad token")),
        pytest.raises(ConnectionError, match="Client initialization failed"),
    ):
        DatabricksConnector(
            server_hostname=SERVER_HOSTNAME,
            http_path=HTTP_PATH,
            access_token=ACCESS_TOKEN,
            catalog=CATALOG,
            schema=SCHEMA,
        )


# ---------------------------------------------------------
# read_data
# ---------------------------------------------------------


def test_read_data_success(connector, mock_engine, sample_dataframe):
    query = "SELECT * FROM fake_table"
    with patch("AnalystStack.connectors.databricks.query.pd.read_sql", return_value=sample_dataframe) as mock_read_sql:
        result_df = connector.read_data(query)

    mock_read_sql.assert_called_once_with(query, mock_engine)
    pd.testing.assert_frame_equal(result_df, sample_dataframe)


def test_read_data_failure(connector, mock_engine):
    with (
        patch("AnalystStack.connectors.databricks.query.pd.read_sql", side_effect=Exception("cluster terminated")),
        pytest.raises(QueryExecutionError, match="Query execution failed: cluster terminated"),
    ):
        connector.read_data("SELECT * FROM fake_table")


# ---------------------------------------------------------
# write_data
# ---------------------------------------------------------


def test_write_data_uses_engine(connector, mock_engine, sample_dataframe):
    with patch("pandas.DataFrame.to_sql") as mock_to_sql:
        connector.write_data(df=sample_dataframe, schema=SCHEMA, table_id="products", if_exists="replace")

    mock_to_sql.assert_called_once_with(
        name="products", con=mock_engine, schema=SCHEMA, if_exists="replace", index=False
    )


def test_write_data_rejects_invalid_table_reference(connector, sample_dataframe):
    with pytest.raises(ValidationError):
        connector.write_data(df=sample_dataframe, schema="bad-schema!", table_id="t")


def test_write_data_rejects_invalid_if_exists(connector, sample_dataframe):
    with pytest.raises(ValueError, match="Invalid if_exists value"):
        connector.write_data(df=sample_dataframe, schema=SCHEMA, table_id="t", if_exists="bogus")


# ---------------------------------------------------------
# metadata & profiling
# ---------------------------------------------------------


def test_get_all_table_names(connector, mock_engine):
    tables_df = pd.DataFrame({"table_name": ["orders", "customers"]})
    with patch("AnalystStack.connectors.databricks.query.pd.read_sql", return_value=tables_df):
        result = connector.get_all_table_names(SCHEMA)
    assert result == ["orders", "customers"]


def test_get_datatypes(connector, mock_engine):
    schema_df = pd.DataFrame({"column_name": ["id", "name", "price"], "data_type": ["BIGINT", "STRING", "DOUBLE"]})
    with patch("AnalystStack.connectors.databricks.query.pd.read_sql", return_value=schema_df):
        result = connector.get_datatypes(SCHEMA, "products")
    assert result == {"id": "BIGINT", "name": "STRING", "price": "DOUBLE"}


def test_get_fillrate(connector, mock_engine):
    schema_df = pd.DataFrame({"column_name": ["id", "name"], "data_type": ["BIGINT", "STRING"]})
    fillrate_df = pd.DataFrame({"id": [100.0], "name": [95.5]})

    with patch("AnalystStack.connectors.databricks.query.pd.read_sql", side_effect=[schema_df, fillrate_df]):
        result = connector.get_fillrate(SCHEMA, "products")
    assert result == {"id": 100.0, "name": 95.5}
