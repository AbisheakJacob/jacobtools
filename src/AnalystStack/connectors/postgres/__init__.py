# import the main class using a relative import (.)
from .connector import PostgresConnector

# the __all__ variable strictly defines waht gets exported if someone runs `from ... import *`
__all__ = ["PostgresConnector"]
