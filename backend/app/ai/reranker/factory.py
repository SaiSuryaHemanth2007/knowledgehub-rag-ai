from app.ai.reranker.base import BaseReranker
from app.ai.reranker.passthrough import PassthroughReranker
from app.core.config import settings


class RerankerFactory:
    """
    Creates the configured reranker implementation.

    The factory keeps provider selection outside the
    retrieval service so different reranker implementations
    can be introduced without modifying the retrieval pipeline.
    """

    @staticmethod
    def create() -> BaseReranker:
        """
        Create a reranker based on application configuration.
        """

        provider = settings.RERANKER_PROVIDER.lower().strip()

        if not settings.RERANKER_ENABLED:
            return PassthroughReranker()

        if provider == "passthrough":
            return PassthroughReranker()

        raise ValueError(
            f"Unsupported reranker provider: {provider}"
        )