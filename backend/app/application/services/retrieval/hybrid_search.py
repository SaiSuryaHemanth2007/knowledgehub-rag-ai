from app.core.config import settings


class HybridSearchService:
    """
    Combines vector and keyword retrieval results
    into a single ranked candidate set.

    Pipeline:

        Vector Results
              +
        Keyword Results
              ↓
        Score Calibration
              ↓
        Weighted Hybrid Score
              ↓
        Ranking
              ↓
        Candidate Top K
              ↓
        Reranker
    """

    def combine(
        self,
        vector_results: list[dict],
        keyword_results: list[dict],
        limit: int = 20,
    ) -> list[dict]:
        """
        Combine vector and keyword retrieval results
        using weighted scoring.

        IMPORTANT:

        This stage is responsible for candidate ranking,
        not final relevance classification.

        The final relevance decision belongs to the
        reranking/grounding stage.

        Therefore, HYBRID_MIN_SCORE is intentionally
        NOT applied here.
        """

        vector_scores = self._build_score_map(
            vector_results
        )

        keyword_scores = self._build_score_map(
            keyword_results
        )

        combined = {}

        # ==================================================
        # Vector Results
        # ==================================================

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

        # ==================================================
        # Keyword Results
        # ==================================================

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

        # ==================================================
        # Calculate Hybrid Scores
        # ==================================================

        results = []

        for item in combined.values():

            vector_score = item[
                "vector_score"
            ]

            keyword_score = item[
                "keyword_score"
            ]

            hybrid_score = (
                vector_score
                * settings.VECTOR_SEARCH_WEIGHT
            ) + (
                keyword_score
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
                        vector_score,
                        4,
                    ),
                    "keyword_score": round(
                        keyword_score,
                        4,
                    ),
                }
            )

        # ==================================================
        # Rank Candidates
        # ==================================================

        results.sort(
            key=lambda result: result["score"],
            reverse=True,
        )

        # ==================================================
        # Return Candidate Pool
        # ==================================================

        return results[:limit]

    # ======================================================
    # Build Score Map
    # ======================================================

    def _build_score_map(
        self,
        results: list[dict],
    ) -> dict[int, float]:
        """
        Build a dictionary mapping chunk IDs
        to their original retrieval scores.

        No min-max normalization is performed.

        Keeping the original scores prevents a weak
        candidate from becoming artificially strong
        merely because it was the best candidate
        within its own retrieval set.
        """

        if not results:
            return {}

        return {
            result["chunk"].id: self._clamp_score(
                float(result["score"])
            )
            for result in results
        }

    # ======================================================
    # Clamp Score
    # ======================================================

    def _clamp_score(
        self,
        score: float,
    ) -> float:
        """
        Keep retrieval scores within the expected
        0.0 - 1.0 range.
        """

        return max(
            0.0,
            min(
                1.0,
                score,
            ),
        )