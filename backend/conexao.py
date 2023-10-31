import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

string_conexao = str(os.getenv('DATABASE_URL_HEROKU'))

engine = create_engine(string_conexao)

def get_session() -> Session:
    session = sessionmaker(bind=engine)
    return session()