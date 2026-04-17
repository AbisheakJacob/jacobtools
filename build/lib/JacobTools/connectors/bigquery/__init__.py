# Import the main class using a relative import (.)
from .connector import GoogleBigQueryConnector

# The __all__ variable strictly defines what gets exported if someone runs `from ... import *`
__all__ = ["GoogleBigQueryConnector"]