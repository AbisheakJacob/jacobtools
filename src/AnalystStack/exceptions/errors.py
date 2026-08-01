class DataPackageError(Exception):
    """Base exception for the package."""


class ConfigurationError(DataPackageError):
    """Raised when configuration/settings are invalid or missing."""


class ConnectionError(DataPackageError):
    """Raised when authentication or client initialization fails."""


class QueryExecutionError(DataPackageError):
    """Raised when a SQL query or DataFrame write operation fails."""


class ValidationError(DataPackageError):
    """Raised when input validation fails (e.g., malformed table names)."""
