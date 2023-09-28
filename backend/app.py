from datetime import datetime

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from .conexao import get_session
from .schemas import CadastrarLoja, ConsultaLojas

app = FastAPI()
templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    now = datetime.now()
    return templates.TemplateResponse(
        'index.html', {'request': request, 'active': 'index', 'now': now}
    )


@app.get('/lojas', response_model=ConsultaLojas)
async def consultar_lojas(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 50,
    ConsultaLojas: ConsultaLojas = Depends(),
):
    lojas = session.scalar(
        select(ConsultaLojas).offset(skip).limit(limit)
    ).all()
    now = datetime.now()
    return RedirectResponse('lojas.html', active='lojas', lojas=lojas, now=now)


@app.route('/cadastro')
async def cadastrar_loja(
    session: Session = Depends(get_session),
    nome_loja: str = Form(),
    cep: str = Form(),
    endereco: str = Form(),
    numero: int = Form(),
    complemento: str = Form(),
    bairro: str = Form(),
    cidade: str = Form(),
    telefone: str = Form(),
    horario_funcionamento: str = Form(),
    descricao: str = Form(),
    imagem: str = Form(),
):
    now = datetime.now()

    validar_loja = session.scalar(
        select(CadastrarLoja).where(CadastrarLoja.nome_loja == nome_loja)
    ).first()

    if validar_loja:
        raise HTTPException(
            status_code=400, detail='Loja já cadastrada no sistema.'
        )
    else:
        loja = CadastrarLoja(
            nome_loja=nome_loja,
            cep=cep,
            endereco=endereco,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            cidade=cidade,
            telefone=telefone,
            horario_funcionamento=horario_funcionamento,
            descricao=descricao,
            imagem=imagem,
        )
        session.add(loja)
        session.commit()
        return RedirectResponse(url='/lojas', status_code=302)

    return RedirectResponse(url='/lojas', status_code=302, now=now)
