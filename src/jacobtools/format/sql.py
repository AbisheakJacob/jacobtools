import os
from typing import Any, Dict, List

import sqlfluff

from JacobTools.utils.logging import get_logger

logger = get_logger(__name__)


class SQLFormatter:
    """Handles SQL linting and formatting using SQLFluff."""

    def __init__(self, dialect: str = "bigquery", templater: str = "jinja", config_path: str = None):
        """
        config_path: Path to a .sqlfluff file containing your preset requirements.
        """
        self.dialect = dialect
        self.templater = templater
        self.config_path = config_path

        # Build the configuration override dictionary
        self.config_overrides = {"core": {"dialect": self.dialect, "templater": self.templater}}

        # If the user has a .sqlfluff file (e.g., in their repo root), point to it
        if self.config_path and os.path.exists(self.config_path):
            logger.info(f"Using SQLFluff config from {self.config_path}")
            self.config = sqlfluff.config.FluffConfig.from_path(self.config_path, overrides=self.config_overrides)
        else:
            self.config = sqlfluff.config.FluffConfig(overrides=self.config_overrides)

    def view_errors(self, sql_string: str) -> List[Dict[str, Any]]:
        """
        Lints the SQL and returns a list of dictionaries detailing the errors
        (line number, position, rule broken, and description).
        """
        logger.info("Linting SQL string...")
        try:
            lint_results = sqlfluff.lint(sql_string, config=self.config)
            if not lint_results:
                logger.info("SQL is clean! No errors found.")
            return lint_results
        except Exception as e:
            logger.error(f"SQLFluff linting failed: {e}")
            raise

    def format_code(self, sql_string: str) -> str:
        """
        Automatically fixes linting errors and formats the SQL string
        based on the preset requirements.
        """
        logger.info("Formatting SQL string...")
        try:
            formatted_sql = sqlfluff.fix(sql_string, config=self.config)
            return formatted_sql
        except Exception as e:
            logger.error(f"SQLFluff formatting failed: {e}")
            raise
