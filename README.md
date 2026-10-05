# TaskFlow API

API REST de gerenciamento de tarefas, com autenticação JWT completa, construída
com foco em boas práticas de arquitetura e testabilidade.

![CI](https://github.com/SEU_USUARIO/taskflow-api/actions/workflows/ci.yml/badge.svg)

## ✨ Funcionalidades

- Registro e login de usuários com senha criptografada (bcrypt)
- Autenticação via JWT (JSON Web Token)
- CRUD completo de tarefas, protegido por autenticação
- Isolamento de dados: cada usuário só acessa suas próprias tarefas
- Documentação automática (Swagger / ReDoc)
- Testes automatizados com pytest
- Pipeline de CI no GitHub Actions
- Pronto para rodar via Docker

## 🧱 Stack técnica

Python · FastAPI · SQLAlchemy · Pydantic · JWT (python-jose) · Passlib (bcrypt) · pytest · Docker

## 📁 Estrutura do projeto

```
taskflow-api/
├── app/
│   ├── main.py          # ponto de entrada da aplicação
│   ├── config.py        # configurações via variáveis de ambiente
│   ├── database.py       # conexão com o banco (SQLAlchemy)
│   ├── models.py          # modelos ORM (User, Task)
│   ├── schemas.py         # schemas Pydantic (validação)
│   ├── auth.py            # hashing de senha e JWT
│   ├── crud.py             # operações de banco de dados
│   └── routers/
│       ├── auth.py        # rotas de autenticação
│       └── tasks.py        # rotas de tarefas
├── tests/                  # testes automatizados (pytest)
├── .github/workflows/      # pipeline de CI
├── Dockerfile
└── docker-compose.yml
```

## 🚀 Como rodar localmente

### 1. Clonar e criar o ambiente virtual

```bash
git clone (https://github.com/edumelob/TaskFlow-API)
cd taskflow-api
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar variáveis de ambiente

```bash
cp .env.example .env
```

### 4. Rodar a aplicação

```bash
uvicorn app.main:app --reload
```

A API estará disponível em `http://localhost:8000`.
Documentação interativa (Swagger): `http://localhost:8000/docs`

## 🐳 Rodando com Docker

```bash
docker compose up --build
```

## ✅ Rodando os testes

```bash
pip install -r requirements-dev.txt
pytest -v
```

## 📌 Endpoints principais

| Método | Rota             | Descrição                          | Autenticação |
|--------|------------------|-------------------------------------|--------------|
| POST   | `/auth/register` | Cria um novo usuário                | Não          |
| POST   | `/auth/login`    | Autentica e retorna um token JWT    | Não          |
| GET    | `/auth/me`       | Retorna o usuário autenticado       | Sim          |
| GET    | `/tasks/`        | Lista as tarefas do usuário         | Sim          |
| POST   | `/tasks/`        | Cria uma nova tarefa                | Sim          |
| GET    | `/tasks/{id}`    | Retorna uma tarefa específica       | Sim          |
| PATCH  | `/tasks/{id}`    | Atualiza parcialmente uma tarefa    | Sim          |
| DELETE | `/tasks/{id}`    | Remove uma tarefa                   | Sim          |

## 🔐 Exemplo de uso (fluxo completo)

```bash
# 1. Registrar um usuário
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "eduardo@email.com", "password": "senhaSegura123"}'

# 2. Fazer login e obter o token
curl -X POST http://localhost:8000/auth/login \
  -F "username=eduardo@email.com" \
  -F "password=senhaSegura123"

# 3. Criar uma tarefa (substitua SEU_TOKEN pelo access_token retornado acima)
curl -X POST http://localhost:8000/tasks/ \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Estudar FastAPI", "description": "Revisar JWT"}'
```

## 🗺️ Possíveis evoluções

- Migrations com Alembic em vez de `create_all`
- Refresh tokens
- Rate limiting
- Deploy em produção (Render / Railway)

---

Projeto desenvolvido por **Eduardo Melo Barbosa** como parte do portfólio de
desenvolvimento backend.
