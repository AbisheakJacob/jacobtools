"""The Facade (The Final Connecter)

This is what your end-users will interact with. it inherits from BaseConnectory to fulfill the contract,
but it offloads the actual work to the managers
"""

from AnalystStack.config.settings import DatabricksSettings
from AnalystStack.connectors.base import BaseConnector
from AnalystStack.connectors.databricks.client import DatabricksClientWrapper
from AnalystStack.exceptions.errors import ConfigurationError


class DatabricksConnector(BaseConnector):
    """Expert-level facade combining client, query, metadata, and profiling logic

    Catalog and schema are not added to the instance as at one point we will not be working
    with multiple catalogs and schemas"""

    def __init__(
        self, server_hostname: str | None = None, http_path: str | None = None, access_token: str | None = None
    ):

        settings = DatabricksSettings()
        self.server_hostname = server_hostname or settings.server_hostname
        self.http_path = http_path or settings.http_path
        self.access_token = access_token or settings.access_token

        if not self.server_hostname or not self.http_path or not self.access_token:
            raise ConfigurationError(
                "A Databricks server_hostname, http_path, and access_token must be provided or set in env variables."
            )

        self._client_wrapper = DatabricksClientWrapper(self.server_hostname, self.http_path, self.access_token)
