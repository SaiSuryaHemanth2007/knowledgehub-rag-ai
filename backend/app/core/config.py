from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings:
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

    GROQ_API_KEY: str

    GROQ_MODEL: str = "openai/gpt-oss-120b"

    # Future Providers

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

    # Number of final chunks returned
    # by the retrieval pipeline.

    RETRIEVAL_LIMIT: int = 5

    # Number of candidates retrieved from
    # each retrieval strategy before hybrid ranking.

    RETRIEVAL_CANDIDATE_LIMIT: int = 20

    # Minimum vector similarity score required
    # for a vector result to be considered.

    RETRIEVAL_MIN_SCORE: float = 0.60

    # ==========================
    # Hybrid Search
    # ==========================

    # Semantic/vector search weight.

    VECTOR_SEARCH_WEIGHT: float = 0.70

    # PostgreSQL keyword search weight.

    KEYWORD_SEARCH_WEIGHT: float = 0.30

    # Optional hybrid relevance threshold.
    #
    # This value is reserved for future relevance
    # filtering and is NOT applied during candidate
    # generation.
    #
    # The reranker is responsible for final
    # relevance selection.

    HYBRID_MIN_SCORE: float = 0.60

    # ==========================
    # Reranking
    # ==========================

    # Enable reranking.

    RERANKER_ENABLED: bool = True

    # Maximum number of hybrid candidates passed
    # to the reranker.

    RERANKER_CANDIDATE_LIMIT: int = 20

    # Number of final chunks returned
    # after reranking.

    RERANKER_TOP_K: int = 5

    # Reranker provider.
    #
    # Currently using the passthrough implementation
    # while the production reranker is being implemented.

    RERANKER_PROVIDER: str = "passthrough"

    # ==========================
    # Logging
    # ==========================

    LOG_LEVEL: str = "INFO"

    # ==========================
    # Pydantic Settings
    # ==========================

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()