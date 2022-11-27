from pathlib import Path
from enum import Enum, auto

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class DBEnv(Enum):
    TESTING = auto()
    STAGING = auto()
    PRODUCTION = auto()


testing_db = Path("app/testing.db")
staging_db = Path("app/staging.db")
prod_db = Path("app/production.db")


# dict mapping enum to relative path of sqlite file
db_files = {
    DBEnv.TESTING: testing_db,
    DBEnv.STAGING: staging_db,
    DBEnv.PRODUCTION: prod_db,
}
# not sure if this Base needs to be diff for each env?
Base = declarative_base()


def get_engine_for(env: DBEnv) -> Engine:
    db_file = db_files.get(env, None)
    if db_file is None:
        raise FileNotFoundError(f"{env} is not a valid DBEnv enum value!")

    connection_url = f"sqlite:///{db_file}"
    return create_engine(connection_url, connect_args={"check_same_thread": False})


def init_db_for(env: DBEnv) -> None:
    _engine = get_engine_for(env)

    Base.metadata.drop_all(bind=_engine)
    Base.metadata.create_all(bind=_engine)


def get_session_for(env: DBEnv) -> sessionmaker:
    _engine = get_engine_for(env)
    return sessionmaker(autocommit=False, autoflush=False, bind=_engine)
# db_file = Path("app/temp.db")
# DATABASE_URL = f"sqlite:///{db_file}"
#
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
#
# def init_db():
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)
