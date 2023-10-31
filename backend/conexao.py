import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

DATABASE_URL_HEROKU = os.getenv('DATABASE_URL_HEROKU')

print(DATABASE_URL_HEROKU)   

engine = create_engine(DATABASE_URL_HEROKU)

def get_session() -> Session:
    session = sessionmaker(bind=engine)
    return session()