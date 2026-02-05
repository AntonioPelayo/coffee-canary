import os
from typing import Optional
import pandas as pd

from .db import _get_engine
from src.db.schema import (
    BEANS_TABLE,
    ROASTERS_TABLE
)


def load_beans_dataframe() -> pd.DataFrame:
    """Load coffee bean records from Postgres if available, otherwise CSV.

    Table name can be set via COFFEE_BEANS_TABLE (defaults to coffee_beans).
    CSV fallback path via COFFEE_BEANS_CSV.
    """
    engine = _get_engine()
    if engine is not None:
        query = f'SELECT * FROM {BEANS_TABLE}'
        try:
            df = pd.read_sql(query, con=engine)
            return df
        except Exception as e:
            print(e)
    # CSV fallback
    csv_path = os.getenv('COFFEE_BEANS_CSV', 'data/coffee_beans.csv')
    try:
        if csv_path and os.path.exists(csv_path):
            return pd.read_csv(csv_path)
    except Exception as e:
        print(e)
    return pd.DataFrame()


def load_roasters_dataframe() -> pd.DataFrame:
    """Load roaster location records from Postgres if available, otherwise CSV."""
    engine = _get_engine()
    if engine is not None:
        query = f'SELECT * FROM {ROASTERS_TABLE}'
        try:
            df = pd.read_sql(query, con=engine)
            return df
        except Exception as e:
            print(e)
    # CSV fallback
    csv_path = os.getenv('COFFEE_ROASTERS_CSV', 'data/coffee_roasters.csv')
    try:
        if csv_path and os.path.exists(csv_path):
            return pd.read_csv(csv_path)
    except Exception as e:
        print(e)
    return pd.DataFrame()


__all__ = [
    'load_beans_dataframe',
    'load_roasters_dataframe',
]