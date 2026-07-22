from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_scheme

def pegar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_scheme), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Acesso negado, verifirique a validade do token")
    # verificar se o token é válido
    # extrair o id do usuário do token
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Acesso inválido")
    return usuario

def verificar_admin(
    usuario: Usuario = Depends(verificar_token),
) -> Usuario:
    if not usuario.ativo:
        raise HTTPException(
            status_code=403,
            detail="Usuário inativo",
        )

    if not usuario.admin:
        raise HTTPException(
            status_code=403,
            detail="Apenas administradores podem executar esta operação",
        )

    return usuario
