"""AnalystStack — reusable helpers for the everyday work of data analysts.

Top-level conveniences::

    from AnalystStack import io, PythonFormatter, SQLFormatter
    from AnalystStack import to_tidy, from_tidy, compare_dataframes, summarize
    from AnalystStack import Validator, not_null, unique, in_range, is_in, matches_regex, has_dtype, custom

Warehouse connectors live under ``AnalystStack.connectors`` and are imported
explicitly (they require optional extras such as ``analyststack[bigquery]``)::

    from AnalystStack.connectors import GoogleBigQueryConnector
"""

from importlib.metadata import PackageNotFoundError, version

from AnalystStack.compare import ComparisonResult, compare_dataframes, summarize
from AnalystStack.format import PythonFormatter, SQLFormatter
from AnalystStack.io import io
from AnalystStack.tidy import from_tidy, to_tidy
from AnalystStack.validate import (
    CheckResult,
    Rule,
    ValidationReport,
    Validator,
    custom,
    has_dtype,
    in_range,
    is_in,
    matches_regex,
    not_null,
    unique,
)

try:
    __version__ = version("AnalystStack")
except PackageNotFoundError:  # package not installed (e.g. running from a source tree)
    __version__ = "0.0.0"

__all__ = [
    "io",
    "PythonFormatter",
    "SQLFormatter",
    "to_tidy",
    "from_tidy",
    "compare_dataframes",
    "summarize",
    "ComparisonResult",
    "Validator",
    "Rule",
    "CheckResult",
    "ValidationReport",
    "not_null",
    "unique",
    "in_range",
    "is_in",
    "matches_regex",
    "has_dtype",
    "custom",
    "__version__",
]
