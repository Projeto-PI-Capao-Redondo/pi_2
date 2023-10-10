from datetime import datetime

from fastapi import Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from .conexao import get_session
from .models import Loja
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
    request: Request,
    session: Session = Depends(get_session),
):
    lojas = session.query(Loja).all()
    now = datetime.now()
    return templates.TemplateResponse(
        'lojas.html',
        {'request': request, 'active': 'lojas', 'now': now, 'lojas': lojas},
    )

@app.get('/entrar', response_class=HTMLResponse)
async def login(request: Request):
    now = datetime.now()
    return templates.TemplateResponse(
        'entrar.html', 
        {'request': request, 'active': 'entrar', 'now': now}
    )


@app.get('/cadastrar_usuario', response_class=HTMLResponse)
async def cadastrar(request: Request):
    now = datetime.now()
    return templates.TemplateResponse(
        'cadastrar_usuario.html',
        {'request': request, 'active': 'cadastrar_usuario', 'now': now},
    )

@app.post('/lojas/cadastrar_loja', response_class=HTMLResponse)
async def cadastrar_loja(
    request: Request,
    session: Session = Depends(get_session),
    nome_loja: str = Form(...),
    cep: str = Form(...),
    endereco: str = Form(...),
    numero: int = Form(...),
    complemento: str = Form(...),
    bairro: str = Form(...),
    cidade: str = Form(...),
    telefone: str = Form(...),
    horario_funcionamento: str = Form(...),
    descricao: str = Form(...),
    imagem: str = Form(...),
):
    now = datetime.now()

    validar_loja = (
        session.query(CadastrarLoja)
        .filter(CadastrarLoja.nome_loja == nome_loja)
        .first()
    )

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

        return templates.TemplateResponse(
            'cadastrar_loja.html',
            {
                'request': request,
                'active': 'cadastrar_loja',
                'now': now,
                'form': Form,
            },
        )


@app.post('/lojas/{id}', response_class=HTMLResponse)
async def alterar_dados_loja(
    request: Request,
    id: int,
    session: Session = Depends(get_session),
):
    now = datetime.now()
    loja = session.scalar(
        select(CadastrarLoja).where(CadastrarLoja.id == id)
    ).first()



