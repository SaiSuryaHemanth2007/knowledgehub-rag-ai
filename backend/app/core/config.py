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

    GOOGLE_API_KEY: str = ""

    GROQ_API_KEY: str = ""

    GROQ_MODEL: str = "openai/gpt-oss-120b"

    OPENAI_API_KEY: str = ""

    ANTHROPIC_API_KEY: str = ""

    # ==========================
    # Embedding
    # ==========================

    EMBEDDING_MODEL: str = "gemini-embedding-001"

    EMBEDDING_DIMENSION: int = 3072

    # ==========================
    # Retrieval
    # ==========================

    RETRIEVAL_LIMIT: int = 5

    RETRIEVAL_CANDIDATE_LIMIT: int = 20

    RETRIEVAL_MIN_SCORE: float = 0.60

    # ==========================
    # Hybrid Search
    # ==========================

    VECTOR_SEARCH_WEIGHT: float = 0.70

    KEYWORD_SEARCH_WEIGHT: float = 0.30

    HYBRID_MIN_SCORE: float = 0.60

    # ==========================
    # Reranking
    # ==========================

    RERANKER_ENABLED: bool = True

    RERANKER_CANDIDATE_LIMIT: int = 20

    RERANKER_TOP_K: int = 5

    RERANKER_PROVIDER: str = "lexical"

    # ==========================
    # Logging
    # ==========================

    LOG_LEVEL: str = "INFO"

    # ==========================
    # Pydantic Settings
    # ==========================

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()