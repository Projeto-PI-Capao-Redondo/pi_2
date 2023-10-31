from datetime import datetime

from fastapi import Cookie, Depends, FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from .conexao import get_session
from .models import Loja, Usuario

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')


def get_current_user(username: str = Cookie(None)):
    return username


@app.get('/', response_class=HTMLResponse)
async def read_item(
    request: Request, current_user: str = Depends(get_current_user)
):
    now = datetime.now()
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'active': 'index',
            'current_user': current_user,
            'now': now,
        },
    )


@app.get('/lojas')
async def consultar_lojas(
    request: Request,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    lojas = session.query(Loja).all()
    now = datetime.now()
    return templates.TemplateResponse(
        'lojas.html',
        {
            'request': request,
            'now': now,
            'lojas': lojas,
            'current_user': current_user,
        },
    )


@app.get('/cadastrar_loja', response_class=HTMLResponse)
async def render_loja(
    request: Request, current_user: str = Depends(get_current_user)
):
    now = datetime.now()
    return templates.TemplateResponse(
        'cadastrar_loja.html',
        {
            'request': request,
            'active': 'cadastrar_loja',
            'now': now,
            'current_user': current_user,
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
    observacao: str = Form(...),
    horario_funcionamento: str = Form(...),
):
    try:
        loja = Loja(
            nome_loja=nome_loja,
            cep=cep,
            rua=rua,
            numero=numero,
            complemento=complemento,
            bairro=bairro,
            observacao=observacao,
            horario_funcionamento=horario_funcionamento,
        )
        session.add(loja)
        session.commit()
        session.refresh(loja)
        return RedirectResponse(url='/lojas', status_code=303)
    except Exception as e:
        return {'error': str(e)}


@app.get('/roteiro', response_class=HTMLResponse)
async def roteiro(
    request: Request,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    now = datetime.now()
    lojas = session.query(Loja).all()
    return templates.TemplateResponse(
        'roteiro.html',
        {
            'request': request,
            'active': 'roteiro',
            'now': now,
            'lojas': lojas,
            'current_user': current_user,
        },
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
    request: Request, current_user: str = Depends(get_current_user)
):
    now = datetime.now()
    return templates.TemplateResponse(
        'entrar.html',
        {
            'request': request,
            'active': 'entrar',
            'now': now,
            'current_user': current_user,
        },
    )


@app.post('/entrar', response_class=HTMLResponse)
async def login(
    session: Session = Depends(get_session),
    email: str = Form(...),
    senha: str = Form(...),
):
    user_db = session.query(Usuario).filter(Usuario.email == email).first()
    if user_db is None:
        raise HTTPException(status_code=401, detail='Usuário não encontrado.')

    response = RedirectResponse(url='/', status_code=303)
    response.set_cookie(key='username', value=user_db.nome)

    return response


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
