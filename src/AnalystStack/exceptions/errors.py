class DataPackageError(Exception):
    """Base exception for the package."""

    pass


class ConfigurationError(DataPackageError):
    """Raised when configuration/settings are invalid or missing."""

    pass


class ConnectionError(DataPackageError):
    """Raised when authentication or client initialization fails."""

    pass


class QueryExecutionError(DataPackageError):
    """Raised when a SQL query or DataFrame write operation fails."""

    pass


class ValidationError(DataPackageError):
    """Raised when input validation fails (e.g., malformed table names)."""

    pass
