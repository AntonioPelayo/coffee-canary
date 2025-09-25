import os
from typing import Optional
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def _get_engine() -> Optional[Engine]:
    """Create a SQLAlchemy engine from environment variables if configured.

    Returns None if insufficient configuration.
    """
    db_url = os.getenv('DB_URL')
    if not db_url:
        host = os.getenv('DB_HOST')
        database = os.getenv('DB_NAME')
        user = os.getenv('DB_USERNAME')
        password = os.getenv('DB_PASSWORD')
        port = os.getenv('DB_PORT', '5432')
        if all([host, database, user, password]):
            db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    if not db_url:
        return None
    try:
        engine = create_engine(db_url, pool_pre_ping=True)
        return engine
    except Exception:
        return None


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


def load_beans_dataframe() -> pd.DataFrame:
    """Load coffee bean records from Postgres if available, otherwise CSV.

    Table name can be set via COFFEE_BEANS_TABLE (defaults to coffee_beans).
    CSV fallback path via COFFEE_BEANS_CSV.
    """
    engine = _get_engine()
    if engine is not None:
        table = os.getenv('COFFEE_BEANS_TABLE')
        if table:
            query = f'SELECT * FROM {table}'
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
        table = os.getenv('COFFEE_ROASTERS_TABLE')
        if table:
            query = f'SELECT * FROM {table}'
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