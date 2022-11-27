from fastapi.testclient import TestClient
from app.api.v1 import issue_service
from app.database.connector import get_sessionmaker_for, DBEnv, init_db_for
from app.database import setup


# create test client for issue service
issue_client = TestClient(issue_service.app)


# override get_db to use testing db sessions
def get_fresh_testing_db():
    """use the 'dependency_overrides' property on the app to replace 'get_db'
    with this function"""
    # reset to fresh database values
    env = DBEnv.TESTING

    init_db_for(env)
    setup.init_issue_records(env)
    maker = get_sessionmaker_for(env)

    try:
        db = maker()
        yield db
    finally:
        db.close()
