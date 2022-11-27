from typing import Generator

from app.database.connector import get_session_for, DBEnv


def get_db() -> Generator:
    """call this to get a Session object for use for execution of
    db requests"""
    maker = get_session_for(DBEnv.STAGING)
    try:
        db = maker()
        yield db
    finally:
        db.close()
