"""
Configurações centrais da aplicação.
Lê valores de variáveis de ambiente (arquivo .env em desenvolvimento).
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Banco de dados
    database_url: str = "sqlite:///./taskflow.db"

    # JWT
    secret_key: str = "CHANGE_THIS_SECRET_KEY_IN_PRODUCTION"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Metadados da API
    api_title: str = "TaskFlow API"
    api_version: str = "1.0.0"

    class Config:
        env_file = ".env"


settings = Settings()
