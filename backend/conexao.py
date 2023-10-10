from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from .settings import Settings

engine = create_engine(Settings().DATABASE_URL_HEROKU)


def get_session() -> Session:
    session = sessionmaker(bind=engine)
    return session()
