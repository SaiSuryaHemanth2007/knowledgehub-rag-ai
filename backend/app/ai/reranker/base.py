from abc import ABC, abstractmethod


class BaseReranker(ABC):
    """
    Abstract interface for document reranking.

    A reranker receives the user's question together
    with retrieved candidate chunks and assigns a
    relevance score to each candidate.

    The implementation is intentionally provider-independent
    so different reranking strategies can be introduced
    later without changing the retrieval pipeline.
    """

    @abstractmethod
    def rerank(
        self,
        query: str,
        candidates: list[dict],
        limit: int = 5,
    ) -> list[dict]:
        """
        Rerank retrieved candidates according to their
        relevance to the query.

        Args:
            query:
                The user's retrieval query.

            candidates:
                Retrieved document chunks. Each candidate
                is expected to contain at least:

                    {
                        "chunk": ChunkModel,
                        "score": float,
                    }

            limit:
                Maximum number of candidates to return.

        Returns:
            A ranked list of candidates.
        """
        raise NotImplementedError