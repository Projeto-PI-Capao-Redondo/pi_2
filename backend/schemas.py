from pydantic import BaseModel, EmailStr


class UsuarioSchema(BaseModel):
    usuario: str
    email: EmailStr
    senha: str


class UsuarioPublico(BaseModel):
    usuario: str
    email: EmailStr


class ConsultaLojas(BaseModel):
    nome: str
    CEP: str
    Rua: str
    Número: str


class CadastrarLoja(BaseModel):
    id: int | None = None
    nome_loja: str
    cep: str
    rua: str
    complemento: str | None = None
    numero: int
    observacao: str | None = None
    bairro: str
    horario_funcionamento: str
    pontos_interesse: str
    resumo_estabelecimento: str | None = None
    link_site_rede_social: str | None = None
    imagem: str | None = None
