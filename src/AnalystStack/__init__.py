"""AnalystStack — reusable helpers for the everyday work of data analysts.

Top-level conveniences::

    from AnalystStack import io, PythonFormatter, SQLFormatter

Warehouse connectors live under ``AnalystStack.connectors`` and are imported
explicitly (they require optional extras such as ``analyststack[bigquery]``)::

    from AnalystStack.connectors import GoogleBigQueryConnector
"""

from importlib.metadata import PackageNotFoundError, version

from AnalystStack.format import PythonFormatter, SQLFormatter
from AnalystStack.io import io

try:
    __version__ = version("AnalystStack")
except PackageNotFoundError:  # package not installed (e.g. running from a source tree)
    __version__ = "0.0.0"

__all__ = ["io", "PythonFormatter", "SQLFormatter", "__version__"]
