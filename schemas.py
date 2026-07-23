from pydantic import BaseModel, Field
from typing import Optional, List


class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str

    class config:
        from_attributes = True

class AdminSchema(BaseModel):
    nome: str
    email: str
    senha: str

    class config:
        from_attributes = True

class PedidoSchema(BaseModel):
    id_usuario: int

    class config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class config:
        from_attributes = True

class ItemPedidoSchema(BaseModel):
    quantidade: int = Field(gt=0)
    sabor: str
    tamanho: str

    class Config:
        from_attributes = True

class ItemPedidoResponseSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float

    class Config:
        from_attributes = True

class ResponsePedidoSchema(BaseModel):
    id: int
    status: str
    preco: float
    itens: List[ItemPedidoResponseSchema]

    class Config:
        from_attributes = True
