from .reader import DataReader
from .writer import DataWriter


class DataIOManager:
    """Facade for all IO operations."""

    def __init__(self):
        self.read = DataReader()
        self.write = DataWriter()


# Instantiate it so users can just import the pre-configured object
io = DataIOManager()

__all__ = ["io"]
