import os
from typing import Any, Dict, List, Optional

import sqlfluff
from sqlfluff.core.config import FluffConfig

from AnalystStack.utils.logging import get_logger

logger = get_logger(__name__)


class SQLFormatter:
    """Handles SQL linting and formatting using SQLFluff."""

    def __init__(self, dialect: str = "bigquery", templater: str = "jinja", config_path: Optional[str] = None):
        """
        config_path: Path to a .sqlfluff file containing your preset requirements.
        """
        self.dialect = dialect
        self.templater = templater
        self.config_path = config_path

        # Build the configuration override dictionary. SQLFluff expects a flat
        # mapping of config keys (not nested under a "core" section).
        self.config_overrides: Dict[str, Any] = {"dialect": self.dialect, "templater": self.templater}

        # If the user has a .sqlfluff file (e.g., in their repo root), point to it
        if self.config_path and os.path.exists(self.config_path):
            logger.info(f"Using SQLFluff config from {self.config_path}")
            self.config = FluffConfig.from_path(self.config_path, overrides=self.config_overrides)
        else:
            self.config = FluffConfig(overrides=self.config_overrides)

    def view_errors(self, file_path: str) -> List[Dict[str, Any]]:
        logger.info(f"Linting SQL file: {file_path}")

        try:
            with open(file_path, "r") as f:
                sql_string = f.read()

            lint_results = sqlfluff.lint(sql_string, config=self.config)

            if not lint_results:
                logger.info("SQL is clean! No errors found.")

            return lint_results

        except Exception as e:
            logger.error(f"SQLFluff linting failed: {e}")
            raise

    def format_code(self, file_path: str, output_path: Optional[str] = None) -> str:
        logger.info(f"Formatting SQL file: {file_path}")

        try:
            with open(file_path, "r") as f:
                sql_string = f.read()

            formatted_sql = sqlfluff.fix(sql_string, config=self.config)

            # Write output
            if output_path:
                with open(output_path, "w") as f:
                    f.write(formatted_sql)
            else:
                # overwrite original file
                with open(file_path, "w") as f:
                    f.write(formatted_sql)

            return formatted_sql

        except Exception as e:
            logger.error(f"SQLFluff formatting failed: {e}")
            raise
