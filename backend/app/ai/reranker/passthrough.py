from app.ai.reranker.base import BaseReranker


class PassthroughReranker(BaseReranker):
    """
    Temporary reranker implementation.

    This implementation does not change the ranking.
    It provides a safe integration point for the
    future production reranker.
    """

    def rerank(
        self,
        query: str,
        candidates: list[dict],
        limit: int = 5,
    ) -> list[dict]:
        """
        Return candidates in their existing ranking order.
        """

        return candidates[:limit]