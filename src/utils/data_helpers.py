import os
from typing import Optional

import pandas as pd

from .db import get_table_dataframe


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Make column names consistent with expected capitalized forms used in charts."""
    if df.empty:
        return df
    rename_map = {}
    for col in df.columns:
        lower = col.lower()
        if lower == 'roast_level':
            rename_map[col] = "Roast Level"
        # if lower.startswith('blend') and col != 'Blend Name':
        #     rename_map[col] = 'Blend Name'
        # if lower in ('weight (g)', 'net weight (g)', 'net weight', 'weight') and col != 'Weight (g)':
        #     rename_map[col] = 'Weight (g)'
    if rename_map:
        df = df.rename(columns=rename_map)
    return df


def _table_setting(env_var: str, default_key: str) -> str:
    """Read a table identifier from the environment with a safe default."""
    value = os.getenv(env_var)
    if value:
        return value
    return default_key


def load_beans_dataframe() -> pd.DataFrame:
    """Load coffee bean records from the warehouse table."""
    table_key = _table_setting("COFFEE_BEANS_TABLE", "warehouse.fact_coffee_beans")
    df = get_table_dataframe(table_key)
    return _normalize_columns(df)


def load_roasters_dataframe() -> pd.DataFrame:
    """Load roaster dimension records from the warehouse table."""
    table_key = _table_setting("COFFEE_ROASTERS_TABLE", "warehouse.dim_roaster")
    return get_table_dataframe(table_key)


def detect_roast_column(df: pd.DataFrame) -> Optional[str]:
    for candidate in ['Roast Level', 'Roast', 'roast_level']:
        if candidate in df.columns:
            return candidate
    return None


__all__ = [
    'load_beans_dataframe',
    'load_roasters_dataframe',
    'detect_roast_column'
]
