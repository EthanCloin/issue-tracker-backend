from app.database.connector import LocalSession


def get_db() -> LocalSession:
    """call this to get a Session object for use for execution of
    db requests"""
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()
