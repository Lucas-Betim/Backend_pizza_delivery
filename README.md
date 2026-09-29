# Pizza Delivery API 🍕

API REST para gerenciamento de usuários e pedidos de uma pizzaria, desenvolvida com FastAPI. O sistema possui autenticação JWT, controle de acesso por perfil, cardápio com preços definidos pelo servidor e gerenciamento completo de pedidos.

## Funcionalidades

- Cadastro e autenticação de usuários
- Senhas armazenadas com hash usando bcrypt
- Autenticação por access token JWT
- Renovação de token
- Controle de acesso entre clientes e administradores
- Criação de administradores restrita a outros administradores
- Cardápio com sabores, tamanhos e preços definidos pela API
- Criação, consulta, finalização e cancelamento de pedidos
- Adição e remoção de itens
- Cálculo automático do valor total do pedido
- Listagem dos pedidos do usuário autenticado
- Listagem geral de pedidos exclusiva para administradores
- Persistência com SQLAlchemy
- Migrações de banco de dados com Alembic
- Compatibilidade com SQLite e PostgreSQL
- Documentação interativa com Swagger

## Tecnologias

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic
- PostgreSQL
- SQLite
- Pydantic
- JWT
- Passlib e bcrypt
- python-dotenv

## Regras de segurança

Contas comuns são sempre criadas com o perfil de cliente. O usuário não pode se cadastrar como administrador enviando esse valor na requisição.

A criação de uma conta administrativa é feita por uma rota protegida, que exige autenticação de outro administrador.

Os preços também não são enviados pelo cliente. A API recebe apenas o sabor, tamanho e quantidade, consulta o preço correspondente no cardápio e calcula o total no servidor.

## Estrutura do projeto

```text
Backend_pizza_delivery/
├── alembic/
│   ├── versions/
│   └── env.py
├── auth_routes.py
├── dependecies.py
├── main.py
├── models.py
├── order_routes.py
├── schemas.py
├── alembic.ini
├── requirements.txt
└── README.md
```

## Como executar localmente

### 1. Clone o repositório

```bash
git clone URL_DO_REPOSITORIO
cd Backend_pizza_delivery
```

### 2. Crie um ambiente virtual

No Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

No Linux ou macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=adicione_uma_chave_secreta_segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///banco.db
```

Para utilizar PostgreSQL:

```env
DATABASE_URL=postgresql://usuario:senha@host:porta/banco
```

O arquivo `.env` não deve ser enviado ao GitHub.

### 5. Execute as migrações

```bash
alembic upgrade head
```

### 6. Inicie a API

```bash
python -m uvicorn main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

## Documentação interativa

Com a aplicação em execução, acesse:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Principais endpoints

### Autenticação

| Método | Endpoint | Descrição | Autenticação |
|---|---|---|---|
| `GET` | `/auth/` | Verifica a rota de autenticação | Não |
| `POST` | `/auth/criar_conta` | Cria uma conta comum | Não |
| `POST` | `/auth/login` | Realiza login com JSON | Não |
| `POST` | `/auth/login-form` | Login pelo formulário OAuth2 | Não |
| `GET` | `/auth/refresh` | Gera um novo access token | Sim |
| `POST` | `/auth/criar_admin` | Cria uma conta administrativa | Admin |

### Pedidos

Todas as rotas de pedidos exigem um token Bearer válido.

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/order/` | Verifica a rota de pedidos |
| `GET` | `/order/cardapio` | Retorna sabores, tamanhos e preços |
| `POST` | `/order/pedido` | Cria um pedido |
| `POST` | `/order/pedido/adicionar-item/{id_pedido}` | Adiciona um item |
| `POST` | `/order/pedido/remover-item/{id_item_pedido}` | Remove um item |
| `GET` | `/order/pedido/{id_pedido}` | Consulta um pedido |
| `GET` | `/order/pedido/finalizar/{id_pedido}` | Finaliza um pedido |
| `GET` | `/order/pedido/cancelar/{id_pedido}` | Cancela um pedido |
| `GET` | `/order/listar/pedidos-usuario` | Lista os pedidos do usuário |
| `GET` | `/order/listar` | Lista todos os pedidos — somente admin |

## Exemplos de requisições

### Criar uma conta

```json
POST /auth/criar_conta

{
  "nome": "João Silva",
  "email": "joao@email.com",
  "senha": "senha_segura"
}
```

### Realizar login

```json
POST /auth/login

{
  "email": "joao@email.com",
  "senha": "senha_segura"
}
```

A resposta contém o token que deve ser enviado nas rotas protegidas:

```text
Authorization: Bearer SEU_ACCESS_TOKEN
```

### Adicionar um item ao pedido

```json
POST /order/pedido/adicionar-item/1

{
  "quantidade": 2,
  "sabor": "CALABRESA",
  "tamanho": "GRANDE"
}
```

O cliente não informa o preço. A API consulta o cardápio, obtém o preço correto e atualiza automaticamente o valor total do pedido.

## Primeiro administrador

Por segurança, a rota `/auth/criar_admin` somente pode ser utilizada por um administrador autenticado.

Em uma instalação nova, o primeiro administrador deve ser configurado diretamente no banco de dados ou por um processo seguro de inicialização. Depois disso, esse administrador poderá cadastrar outros por meio da rota protegida.

## Estados do pedido

Um pedido pode possuir os seguintes estados:

- `PENDENTE`
- `FINALIZADO`
- `CANCELADO`

Clientes podem consultar e modificar somente os próprios pedidos. Administradores podem consultar e gerenciar todos os pedidos.

## Melhorias futuras

- Transferir o cardápio para tabelas no banco de dados
- Criar gerenciamento administrativo de produtos e preços
- Adicionar endereços de entrega
- Implementar formas de pagamento
- Criar testes automatizados
- Adicionar imagens aos produtos
- Desenvolver uma interface web ou aplicativo
- Substituir rotas de alteração por métodos `PATCH` ou `DELETE`

## Autor

Desenvolvido por **SEU NOME** como projeto de estudo e prática em desenvolvimento backend com Python e FastAPI.
