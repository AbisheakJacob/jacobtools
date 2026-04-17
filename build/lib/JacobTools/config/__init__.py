# Import the main class using a relative import (.)
from .settings import BigQuerySettings

# The __all__ variable strictly defines what gets exported if someone runs `from ... import *`
__all__ = ["BigQuerySettings"]
