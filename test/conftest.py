"""Shared pytest fixtures for the AnalystStack test suite."""

import pandas as pd
import pytest


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """A small, well-formed DataFrame reused across IO and connector tests."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "name": ["Sneaker A", "Sneaker B", "Sneaker C"],
            "price": [99.0, 120.5, None],
        }
    )
