import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

HOST = os.getenv('HOST')
SENHA = os.getenv('SENHA')
BANCO = os.getenv('BANCO')

string_conexao = f"{BANCO}:{HOST}/{SENHA}"

engine = create_engine(string_conexao)

def get_session() -> Session:
    session = sessionmaker(bind=engine)
    return session()