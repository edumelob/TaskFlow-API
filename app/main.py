"""
Ponto de entrada da aplicação FastAPI.
Roda com: uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import auth, tasks

# Cria as tabelas no banco (abordagem simples; em produção, prefira Alembic para migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=(
        "API REST de gerenciamento de tarefas com autenticação JWT completa. "
        "Projeto de portfólio construído com FastAPI, SQLAlchemy e boas práticas "
        "de arquitetura (camadas separadas, testes automatizados, CI/CD)."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção, restrinja aos domínios reais do front-end
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)


@app.get("/", tags=["Status"])
def health_check():
    """Endpoint simples para checar se a API está no ar."""
    return {"status": "ok", "service": settings.api_title, "version": settings.api_version}
