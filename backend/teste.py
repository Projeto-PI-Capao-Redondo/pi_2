

from conexao import get_session
from models import Loja


session = get_session()

lojas = (
        session.query(Loja)
        .all()
    )

print(lojas)