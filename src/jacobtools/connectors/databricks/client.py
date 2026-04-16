from databricks import sql
# package: databricks-sql-connector
from JacobTools.exceptions.errors import ConnectionError
from JacobTools.utils.logging import get_logger

logger = get_logger(__name__)


class DatabricksClientWrapper:
    """Wraps the Databricks client securely"""

    def __init__(
            self,
            server_hostname: str,
            http_path: str,
            access_token: str
            ):
        
        self.server_hostname = server_hostname
        self.http_path = http_path
        self.access_token = access_token

        try:
            self._client = sql.connect(
                server_hostname=self.server_hostname,
                http_path=self.http_path,
                access_token=self.access_token
            )

            logger.info(f"Databricks client initialized for server hostname {self.server_hostname}")
        
        except Exception as e:
            logger.error(f"Failed to initialize Databricks client: {e}")
            raise ConnectionError(f"Client Initialization Falied: {e}")
        
        @property
        def client(self) -> databricks.Client:
            return self._client
