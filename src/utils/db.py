import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

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
