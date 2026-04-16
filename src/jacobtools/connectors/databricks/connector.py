"""The Facade (The Final Connecter)

This is what your end-users will interact with. it inherits from BaseConnectory to fulfill the contract, but it offloads the actual work to the managers
"""

from typing import Optional

from JacobTools.connectors.base import BaseConnector


class DatabricksConnector(BaseConnector):
    """Expert-level facade combining client, query, metadata, and profiling logic"""

    def __init__(
            self,
            server_hostname: Optional[str] = None,
            http_path: Optional[str] = None,
            access_token: Optional[str] = None
            ):
        self.server_hostname = server_hostname
        self.http_path = http_path
        self.access_token = access_token
