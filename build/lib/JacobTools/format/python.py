import ast
import black
from typing import List
from JacobTools.utils.logging import get_logger

logger = get_logger(__name__)

class PythonFormatter:
    """Handles Python linting and formatting using Black and AST."""

    def __init__(self, line_length: int = 100):
        self.mode = black.Mode(line_length=line_length)

    def view_errors(self, code_string: str) -> List[str]:
        """
        Checks for fundamental Python syntax errors without executing the code.
        Returns a list of error messages (empty if clean).
        """
        errors = []
        try:
            ast.parse(code_string)
            logger.info("Python syntax is clean!")
        except SyntaxError as e:
            error_msg = f"SyntaxError on line {e.lineno}, col {e.offset}: {e.msg}\nCode: {e.text}"
            errors.append(error_msg)
            logger.warning(error_msg)
        return errors

    def format_code(self, code_string: str) -> str:
        """
        Formats Python code using Black's uncompromising standards.
        """
        logger.info("Formatting Python string...")
        try:
            # Black expects a trailing newline to function properly
            if not code_string.endswith("\n"):
                code_string += "\n"
            
            formatted_code = black.format_str(code_string, mode=self.mode)
            return formatted_code
        except black.NothingChanged:
            logger.info("Code is already formatted.")
            return code_string
        except Exception as e:
            logger.error(f"Black formatting failed (Check for syntax errors first): {e}")
            raise