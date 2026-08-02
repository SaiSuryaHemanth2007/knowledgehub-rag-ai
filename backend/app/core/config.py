from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ==========================
    # Application
    # ==========================
    APP_NAME: str = "KnowledgeHub RAG AI"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "Enterprise-grade Retrieval-Augmented Generation (RAG) platform."
    )

    # ==========================
    # Environment
    # ==========================
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # ==========================
    # Server
    # ==========================
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # ==========================
    # Database
    # ==========================
    DATABASE_URL: str = (
    "postgresql+psycopg://postgres:postgres@localhost:5432/knowledgehub"
    )

    # ==========================
    # Security
    # ==========================
    SECRET_KEY: str = "CHANGE_ME"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # ==========================
    # AI Providers
    # ==========================
    GROQ_API_KEY: str = ""

    # Future
    OPENAI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""

    # ==========================
    # Logging
    # ==========================
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()