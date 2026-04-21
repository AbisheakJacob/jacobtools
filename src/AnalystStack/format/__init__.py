from .python import PythonFormatter
from .sql import SQLFormatter


class CodeFormatManager:
    """Facade for all code formatting and linting operations."""

    def __init__(self, sql_config_path: str = None):
        # You can pass a path to a .sqlfluff file here
        self.sql = SQLFormatter(config_path=sql_config_path)
        self.python = PythonFormatter()


# Instantiate the facade
format_code = CodeFormatManager()

__all__ = ["format_code", "CodeFormatManager"]
