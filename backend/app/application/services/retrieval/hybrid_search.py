from app.core.config import settings


class HybridSearchService:
    """
    Combines vector and keyword retrieval results
    into a single ranked candidate set.

    Supports multi-query retrieval by preserving:

        primary_score
        secondary_score

    when those scores are available.

    Pipeline:

        Primary Vector Results
              +
        Secondary Vector Results
              +
        Keyword Results
              ↓
        Score Fusion
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
        Combine vector and keyword retrieval results.

        Vector results may contain:

            primary_score
            secondary_score

        These values are preserved during fusion so that
        downstream diagnostics and reranking can use them.

        IMPORTANT:

        HYBRID_MIN_SCORE is intentionally NOT applied here.

        This stage creates the candidate pool.
        Final relevance decisions belong to the reranker.
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

            item = combined.get(chunk_id)

            if item is None:

                item = {
                    "chunk": chunk,
                    "vector_score": 0.0,
                    "keyword_score": 0.0,
                    "primary_score": 0.0,
                    "secondary_score": 0.0,
                }

                combined[chunk_id] = item

            item["vector_score"] = max(
                item["vector_score"],
                vector_scores.get(
                    chunk_id,
                    0.0,
                ),
            )

            # ----------------------------------------------
            # Preserve multi-query scores
            # ----------------------------------------------

            if "primary_score" in result:

                item["primary_score"] = max(
                    item["primary_score"],
                    self._clamp_score(
                        float(
                            result.get(
                                "primary_score",
                                0.0,
                            )
                        )
                    ),
                )

            if "secondary_score" in result:

                item["secondary_score"] = max(
                    item["secondary_score"],
                    self._clamp_score(
                        float(
                            result.get(
                                "secondary_score",
                                0.0,
                            )
                        )
                    ),
                )

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
                    "primary_score": 0.0,
                    "secondary_score": 0.0,
                }

            combined[chunk_id][
                "keyword_score"
            ] = max(
                combined[chunk_id]["keyword_score"],
                keyword_scores.get(
                    chunk_id,
                    0.0,
                ),
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

            primary_score = item[
                "primary_score"
            ]

            secondary_score = item[
                "secondary_score"
            ]

            # ------------------------------------------------
            # Normal hybrid score
            # ------------------------------------------------

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

                    "primary_score": round(
                        primary_score,
                        4,
                    ),

                    "secondary_score": round(
                        secondary_score,
                        4,
                    ),
                }
            )

        # ==================================================
        # Rank Candidates
        # ==================================================

        results.sort(
            key=lambda result: (
                result["score"],
                result["secondary_score"],
                result["primary_score"],
            ),
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
        to their retrieval scores.

        No min-max normalization is performed.

        Keeping original scores prevents a weak candidate
        from becoming artificially strong merely because it
        was the best candidate within its own retrieval set.
        """

        if not results:
            return {}

        return {
            result["chunk"].id: self._clamp_score(
                float(
                    result.get(
                        "score",
                        0.0,
                    )
                )
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