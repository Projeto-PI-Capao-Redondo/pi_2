from sqlalchemy import select

from backend.models import Loja


def test_criar_loja(session):
    nova_loja = Loja(
        id=1,
        nome_loja='teste',
        cep='12345678',
        rua='rua',
        complemento='complemento',
        numero=1,
        observacao='observacao',
        bairro='bairro',
        horario_funcionamento='horario_funcionamento',
        pontos_interesse='pontos_interesse',
        resumo_estabelecimento='resumo_estabelecimento',
        link_site_rede_social='link_site_rede_social',
        imagem='imagem',
    )
    session.add(nova_loja)
    session.commit()

    test = session.scalar(select(Loja).where(Loja.nome_loja == 'teste'))

    assert test.nome_loja == 'teste'
