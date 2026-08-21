from app.core.config import settings


class HybridSearchService:
    """
    Combines vector and keyword retrieval results
    into a single ranked result set.
    """

    def combine(
        self,
        vector_results: list[dict],
        keyword_results: list[dict],
        limit: int = 5,
    ) -> list[dict]:
        """
        Combine vector and keyword results using
        normalized weighted scoring.
        """

        vector_scores = self._normalize_scores(
            vector_results
        )

        keyword_scores = self._normalize_scores(
            keyword_results
        )

        combined = {}

        # ===================================================
        # Vector Results
        # ===================================================

        for result in vector_results:

            chunk = result["chunk"]

            chunk_id = chunk.id

            combined[chunk_id] = {
                "chunk": chunk,
                "vector_score": vector_scores.get(
                    chunk_id,
                    0.0,
                ),
                "keyword_score": 0.0,
            }

        # ===================================================
        # Keyword Results
        # ===================================================

        for result in keyword_results:

            chunk = result["chunk"]

            chunk_id = chunk.id

            if chunk_id not in combined:

                combined[chunk_id] = {
                    "chunk": chunk,
                    "vector_score": 0.0,
                    "keyword_score": 0.0,
                }

            combined[chunk_id][
                "keyword_score"
            ] = keyword_scores.get(
                chunk_id,
                0.0,
            )

        # ===================================================
        # Calculate Hybrid Score
        # ===================================================

        results = []

        for item in combined.values():

            hybrid_score = (
                item["vector_score"]
                * settings.VECTOR_SEARCH_WEIGHT
            ) + (
                item["keyword_score"]
                * settings.KEYWORD_SEARCH_WEIGHT
            )

            results.append(
                {
                    "chunk": item["chunk"],
                    "score": round(
                        hybrid_score,
                        4,
                    ),
                    "vector_score": round(
                        item["vector_score"],
                        4,
                    ),
                    "keyword_score": round(
                        item["keyword_score"],
                        4,
                    ),
                }
            )

        # ===================================================
        # Rank Results
        # ===================================================

        results.sort(
            key=lambda result: result["score"],
            reverse=True,
        )

        return results[:limit]

    # =======================================================
    # Normalize Scores
    # =======================================================

    def _normalize_scores(
        self,
        results: list[dict],
    ) -> dict[int, float]:
        """
        Normalize scores using min-max normalization.
        """

        if not results:
            return {}

        scores = [
            float(result["score"])
            for result in results
        ]

        minimum = min(scores)
        maximum = max(scores)

        # ---------------------------------------------------
        # All scores identical
        # ---------------------------------------------------

        if maximum == minimum:

            return {
                result["chunk"].id: 1.0
                for result in results
            }

        normalized = {}

        for result in results:

            score = float(
                result["score"]
            )

            normalized[
                result["chunk"].id
            ] = (
                (score - minimum)
                / (maximum - minimum)
            )

        return normalized