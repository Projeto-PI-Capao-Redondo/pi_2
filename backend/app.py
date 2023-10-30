from datetime import datetime

from fastapi import Depends, FastAPI, Form, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from . import models
from .conexao import get_session
from .models import Loja, Usuario
from .schemas import (
    CadastrarLoja,
    ConsultaLojas,
    UsuarioPublico,
    UsuarioSchema,
)

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    now = datetime.now()
    return templates.TemplateResponse(
        'index.html', {'request': request, 'active': 'index', 'now': now}
    )


@app.get('/lojas')
async def consultar_lojas(
    request: Request,
    session: Session = Depends(get_session),
):
    lojas = session.query(Loja).all()
    now = datetime.now()
    return templates.TemplateResponse(
        'lojas.html',
        {'request': request, 'now': now, 'lojas': lojas},
    )


@app.get('/cadastrar_loja', response_class=HTMLResponse)
async def render_loja(request: Request):
    now = datetime.now()
    return templates.TemplateResponse(
        'cadastrar_loja.html',
        {
            'request': request,
            'active': 'cadastrar_loja',
            'now': now,
        },
    )


@app.post('/cadastrar_loja')
async def cadastrar_loja(
    session: Session = Depends(get_session),
    nome_loja: str = Form(...),
    cep: str = Form(...),
    rua: str = Form(...),
    numero: int = Form(...),
    complemento: str = Form(...),
    bairro: str = Form(...),
):
    try:
        loja = Loja(
            nome_loja=nome_loja,
            cep=cep,
            rua=rua,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
        )
        session.add(loja)
        session.commit()
        session.refresh(loja)
        return RedirectResponse(url='/lojas', status_code=303)
    except Exception as e:
        return {'error': str(e)}


@app.get('/roteiro', response_class=HTMLResponse)
async def roteiro(request: Request, session: Session = Depends(get_session)):
    now = datetime.now()
    lojas = session.query(Loja).all()
    return templates.TemplateResponse(
        'roteiro.html',
        {'request': request, 'active': 'roteiro', 'now': now, 'lojas': lojas},
    )


@app.post('/lojas/excluir_loja/{id}')
async def excluir_loja(id: int, session: Session = Depends(get_session)):
    """Remove uma loja do banco de dados."""
    try:
        loja = session.query(Loja).filter(Loja.id == id).first()
        if loja is not None:
            session.delete(loja)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail='Loja não encontrada')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/entrar', response_class=HTMLResponse)
async def login(
    request: Request,
    session: Session = Depends(get_session),
):
    now = datetime.now()
    return templates.TemplateResponse(
        'entrar.html', {'request': request, 'active': 'entrar', 'now': now}
    )


@app.get('/cadastrar_usuario', response_class=HTMLResponse)
async def cadastrar(request: Request):
    now = datetime.now()
    return templates.TemplateResponse(
        'cadastrar_usuario.html',
        {'request': request, 'active': 'cadastrar_usuario', 'now': now},
    )


@app.post('/cadastrar_usuario')
async def testecriaruser(
    session: Session = Depends(get_session),
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
):
    try:
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        session.add(novo_usuario)
        session.commit()
        return RedirectResponse(url='/entrar', status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
