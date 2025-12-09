import os
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

def _get_engine() -> Optional[Engine | None]:
    """Create a SQLAlchemy engine from environment variables if configured.

    Returns None if insufficient configuration.
    """
    db_url = os.getenv('DB_URL', 'sqlite:///data/coffee_canary.db')
    if not db_url:
        return None
    try:
        engine = create_engine(db_url, pool_pre_ping=True)
        return engine
    except Exception:
        return None
