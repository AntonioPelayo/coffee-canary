import os
from typing import Dict, Optional, Tuple

import pandas as pd
from sqlalchemy import MetaData, Table, create_engine, select, text
from sqlalchemy.engine import Engine

_ALLOWED_TABLES: Dict[str, Tuple[str, str]] = {
    # Roasters
    "staging.roasters_raw": ("staging", "roasters_raw"),
    "roasters_raw": ("staging", "roasters_raw"),
    "warehouse.dim_roaster": ("warehouse", "dim_roaster"),
    "dim_roaster": ("warehouse", "dim_roaster"),
    "coffee_roasters": ("warehouse", "dim_roaster"),
    # Beans
    "staging.beans_raw": ("staging", "beans_raw"),
    "beans_raw": ("staging", "beans_raw"),
    "warehouse.fact_coffee_beans": ("warehouse", "fact_coffee_beans"),
    "fact_coffee_beans": ("warehouse", "fact_coffee_beans"),
    "coffee_beans": ("warehouse", "fact_coffee_beans")
}


def _get_engine() -> Optional[Engine | None]:
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


def _resolve_table(table_key: str) -> Optional[Tuple[str, str]]:
    """Resolve a user-friendly table identifier to a (schema, table) tuple."""
    normalized = table_key.strip().lower()
    if normalized in _ALLOWED_TABLES:
        return _ALLOWED_TABLES[normalized]
    if "." not in normalized:
        for dotted, resolved in _ALLOWED_TABLES.items():
            if dotted.split(".", 1)[1] == normalized:
                return resolved
    return None


def list_tables():
    """List table names in the connected database, or None if not available."""
    engine = _get_engine()
    if engine is not None:
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_schema, table_name
                FROM information_schema.tables
                WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
                ORDER BY table_schema, table_name;
            """))
            return [f"{row[0]}.{row[1]}" for row in result.fetchall()]
    return None


def get_table_dataframe(table_key: str, limit: Optional[int] = None) -> pd.DataFrame:
    """Fetch an allowed table into a DataFrame, optionally limiting rows."""
    resolved = _resolve_table(table_key)
    if resolved is None:
        raise ValueError(f"Table '{table_key}' is not in the allowed list.")

    engine = _get_engine()
    if engine is None:
        raise RuntimeError("Database engine is not configured.")

    schema, table_name = resolved
    metadata = MetaData()
    table = Table(table_name, metadata, schema=schema, autoload_with=engine)
    stmt = select(table)
    if limit is not None:
        stmt = stmt.limit(limit)

    with engine.connect() as conn:
        return pd.read_sql(stmt, conn)


__all__ = ["_get_engine", "list_tables", "get_table_dataframe"]
