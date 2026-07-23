from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependecies import pegar_sessao, verificar_token
from schemas import ItemPedidoSchema, ResponsePedidoSchema 
from models import Pedido, Usuario, ItemPedido
from typing import List

order_router = APIRouter(prefix="/order", tags=["order"], dependencies=[Depends(verificar_token)])

CARDAPIO = {
    "CALABRESA": {"PEQUENA": 25.0, "MEDIA": 35.0, "GRANDE": 45.0},
    "MUSSARELA": {"PEQUENA": 23.0, "MEDIA": 33.0, "GRANDE": 43.0},
    "MARGUERITA": {"PEQUENA": 27.0, "MEDIA": 37.0, "GRANDE": 47.0},
}

@order_router.get("/")
async def orders():
    '''
    Essa é a rota padrão de pedidos do sistema. todas as rotas dos pedidos precisam de autenticação
    '''
    return {"mensagem": "Você acessou a rota de pedidos"}

@order_router.post("/pedido", status_code=201)
async def criar_pedido(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    novo_pedido = Pedido(usuario=usuario.id)
    session.add(novo_pedido)
    session.commit()
    session.refresh(novo_pedido)
    return {"mensagem": "Pedido criado com sucesso", "pedido_id": novo_pedido.id}

@order_router.get("/cardapio")
async def visualizar_cardapio():
    return {"pizzas": CARDAPIO}

@order_router.get("/pedido/cancelar/{id_pedido}") 
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    # usuario.admin = True
    # usuario.id = pedido.usuario
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não está autorizado para fazer essa modificação")
    pedido.status = "CANCELADO"
    session.commit()
    return {"mensagem": f"pedido {pedido.id} cancelado com sucesso.", "pedido": pedido}

@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não está autorizado para fazer essa operação")
    else:
        pedidos = session.query(Pedido).all()
        return {
            "pedidos": pedidos
            }
    
@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item(id_pedido: int, item_pedido_schema: ItemPedidoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não está autorizado para fazer essa modificação")
    sabor = item_pedido_schema.sabor.strip().upper()
    tamanho = item_pedido_schema.tamanho.strip().upper()

    try:
        preco_unitario = CARDAPIO[sabor][tamanho]
    except KeyError:
        raise HTTPException(
            status_code=400,
            detail="Sabor ou tamanho não disponível no cardápio",
        )

    item_pedido = ItemPedido(
        item_pedido_schema.quantidade,
        sabor,
        tamanho,
        preco_unitario,
        id_pedido,
    )
    session.add(item_pedido)
    session.flush()
    pedido.preco = sum(
        item.preco_unitario * item.quantidade
        for item in session.query(ItemPedido)
        .filter(ItemPedido.pedido==id_pedido)
        .all()
    )
    session.commit()
    session.refresh(item_pedido)
    
    return {"mensagem": f"item adicionado com sucesso ao pedido {id_pedido}", "item_id": item_pedido.id, "preco_pedido": pedido.preco}

@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int, 
                                session: Session = Depends(pegar_sessao), 
                                usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item no pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação")
    session.delete(item_pedido)
    session.flush()
    pedido.preco = sum(
        item.preco_unitario * item.quantidade
        for item in session.query(ItemPedido)
        .filter(ItemPedido.pedido==pedido.id)
        .all()
    )
    session.commit()
    return {
        "mensagem": "Item removido com sucesso",
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

# finalizar pedido
@order_router.get("/pedido/finalizar/{id_pedido}") 
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    # usuario.admin = True
    # usuario.id = pedido.usuario
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não está autorizado para fazer essa modificação")
    pedido.status = "FINALIZADO"
    session.commit()
    return {"mensagem": f"pedido {pedido.id} finalizado com sucesso.", "pedido": pedido}


# visualizar 1 pedido
@order_router.get("/pedido/{id_pedido}")
async def visualizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não está autorizado para fazer essa modificação")
    return {
            "quantidade_itens_pedido": len(pedido.itens),
            "pedido": pedido
        }  
    

# visualizar todos os pedidos de 1 usuario
@order_router.get("/listar/pedidos-usuario", response_model=List[ResponsePedidoSchema])
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
        pedidos = session.query(Pedido).filter(Pedido.usuario==usuario.id).all()
        return pedidos
