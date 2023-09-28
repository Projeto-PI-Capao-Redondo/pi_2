from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Loja(Base):
    __tablename__ = 'loja'

    id: Mapped[int] = mapped_column('id', nullable=False, primary_key=True)
    nome_loja: Mapped[str]
    cep: Mapped[str] = mapped_column('cep', nullable=False)
    rua: Mapped[str]
    complemento: Mapped[str]
    numero: Mapped[int]
    observacao: Mapped[str]
    bairro: Mapped[str]
    horario_funcionamento: Mapped[str]
    pontos_interesse: Mapped[str]
    resumo_estabelecimento: Mapped[str]
    link_site_rede_social: Mapped[str]
    imagem: Mapped[str]


class Usuario(Base):
    __tablename__ = 'usuario'

    id: Mapped[int] = mapped_column('id', nullable=False, primary_key=True)
    nome: Mapped[str]
    email: Mapped[str]
    senha: Mapped[str]
    tipo_usuario: Mapped[str]
