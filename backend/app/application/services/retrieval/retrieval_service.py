from sqlalchemy.orm import Session

from app.ai.reranker.factory import (
    RerankerFactory,
)
from app.application.services.embeddings.embedding_service import (
    EmbeddingService,
)
from app.application.services.retrieval.hybrid_search import (
    HybridSearchService,
)
from app.core.config import settings
from app.infrastructure.repositories.chunk_repository import (
    ChunkRepository,
)


class RetrievalService:
    """
    Advanced retrieval service.

    Retrieval pipeline:

        Question
            ↓
        Conversation History
            ↓
        Primary Retrieval Query
            ↓
        Secondary Intent Query
            ↓
        Multi-Query Vector Search
            ↓
        Candidate Fusion
            ↓
        Hybrid Scoring
            ↓
        Lexical / Concept / Definition Reranking
            ↓
        Final Relevance Gate
            ↓
        Final Top K
    """

    def __init__(
        self,
        db: Session,
    ):
        self.embedding_service = EmbeddingService()

        self.chunk_repository = ChunkRepository(
            db
        )

        self.hybrid_search = HybridSearchService()

        self.reranker = RerankerFactory.create()

    # =======================================================
    # Build Conversation-Aware Retrieval Query
    # =======================================================

    def _build_retrieval_query(
        self,
        question: str,
        history: list | None = None,
    ) -> str:
        """
        Build a focused retrieval query.

        Example:

            Topic: What is generative AI?
            Intent: applications, use cases, examples,
                    business functions
            Question: What are its main applications?
        """

        question = (
            question or ""
        ).strip()

        if not question:
            return ""

        if not history:
            return question

        recent_history = history[-6:]

        user_messages = []

        for message in recent_history:

            if isinstance(
                message,
                dict,
            ):
                role = message.get(
                    "role",
                    "",
                )

                content = message.get(
                    "content",
                    "",
                )

            else:
                role = getattr(
                    message,
                    "role",
                    "",
                )

                content = getattr(
                    message,
                    "content",
                    "",
                )

            if role != "user":
                continue

            if not content:
                continue

            content = str(
                content
            ).strip()

            if content:
                user_messages.append(
                    content
                )

        if not user_messages:
            return question

        previous_question = user_messages[-1]

        intent_terms = (
            self._expand_follow_up_query(
                question
            )
        )

        if not intent_terms:

            history_parts = []

            for message in recent_history:

                if isinstance(
                    message,
                    dict,
                ):
                    role = message.get(
                        "role",
                        "",
                    )

                    content = message.get(
                        "content",
                        "",
                    )

                else:
                    role = getattr(
                        message,
                        "role",
                        "",
                    )

                    content = getattr(
                        message,
                        "content",
                        "",
                    )

                if role not in {
                    "user",
                    "assistant",
                }:
                    continue

                if not content:
                    continue

                content = str(
                    content
                ).strip()

                if not content:
                    continue

                history_parts.append(
                    f"{role}: {content}"
                )

            if not history_parts:
                return question

            context = "\n".join(
                history_parts
            )

            return (
                f"Conversation context:\n"
                f"{context}\n\n"
                f"Current question:\n"
                f"{question}"
            )

        return (
            f"Topic: {previous_question}\n"
            f"Intent: {intent_terms}\n"
            f"Question: {question}"
        )

    # =======================================================
    # Follow-Up Intent Expansion
    # =======================================================

    def _expand_follow_up_query(
        self,
        question: str,
    ) -> str:
        """
        Expand common follow-up questions into
        retrieval-friendly concepts.
        """

        normalized = (
            question or ""
        ).lower().strip()

        if not normalized:
            return ""

        # ---------------------------------------------------
        # Applications / Use Cases
        # ---------------------------------------------------

        application_patterns = (
            "application",
            "applications",
            "use case",
            "use cases",
            "uses",
            "used for",
            "used in",
            "where is it used",
            "where is this used",
            "what can it be used for",
            "what are its uses",
        )

        if any(
            pattern in normalized
            for pattern in application_patterns
        ):
            return (
                "applications, "
                "use cases, "
                "examples, "
                "business functions"
            )

        # ---------------------------------------------------
        # Benefits
        # ---------------------------------------------------

        benefit_patterns = (
            "benefit",
            "benefits",
            "advantage",
            "advantages",
            "why is it useful",
            "why is this useful",
        )

        if any(
            pattern in normalized
            for pattern in benefit_patterns
        ):
            return (
                "benefits, "
                "advantages, "
                "value, "
                "impact"
            )

        # ---------------------------------------------------
        # Examples
        # ---------------------------------------------------

        example_patterns = (
            "example",
            "examples",
            "give me an example",
            "give examples",
            "what are some examples",
        )

        if any(
            pattern in normalized
            for pattern in example_patterns
        ):
            return (
                "examples, "
                "use cases, "
                "practical examples"
            )

        # ---------------------------------------------------
        # Features
        # ---------------------------------------------------

        feature_patterns = (
            "feature",
            "features",
            "capabilities",
            "capability",
            "what can it do",
            "what does it do",
        )

        if any(
            pattern in normalized
            for pattern in feature_patterns
        ):
            return (
                "features, "
                "capabilities, "
                "functionality"
            )

        # ---------------------------------------------------
        # Comparison
        # ---------------------------------------------------

        comparison_patterns = (
            "difference",
            "differences",
            "different from",
            "compare",
            "comparison",
            "versus",
            "vs",
        )

        if any(
            pattern in normalized
            for pattern in comparison_patterns
        ):
            return (
                "comparison, "
                "differences, "
                "similarities, "
                "advantages"
            )

        # ---------------------------------------------------
        # Definition
        # ---------------------------------------------------

        definition_patterns = (
            "what is",
            "what are",
            "define",
            "definition",
            "meaning",
            "explain",
        )

        if any(
            pattern in normalized
            for pattern in definition_patterns
        ):
            return (
                "definition, "
                "meaning, "
                "concept, "
                "fundamentals"
            )

        return ""

    # =======================================================
    # Build Secondary Retrieval Query
    # =======================================================

    def _build_secondary_retrieval_query(
        self,
        question: str,
        history: list | None = None,
    ) -> str:
        """
        Build an intent-focused retrieval query.

        Example:

            Generative AI applications use cases
            business functions customer support
            sales marketing data analysis reporting
        """

        if not history:
            return ""

        intent_terms = (
            self._expand_follow_up_query(
                question
            )
        )

        if not intent_terms:
            return ""

        topic = ""

        recent_history = history[-6:]

        for message in reversed(
            recent_history
        ):

            if isinstance(
                message,
                dict,
            ):
                role = message.get(
                    "role",
                    "",
                )

                content = message.get(
                    "content",
                    "",
                )

            else:
                role = getattr(
                    message,
                    "role",
                    "",
                )

                content = getattr(
                    message,
                    "content",
                    "",
                )

            if role != "user":
                continue

            if not content:
                continue

            topic = str(
                content
            ).strip()

            if topic:
                break

        if not topic:
            return ""

        return (
            f"{topic} "
            f"{intent_terms} "
            f"customer support "
            f"sales marketing "
            f"data analysis reporting"
        )

    # =======================================================
    # Candidate Fusion
    # =======================================================

    def _merge_candidate_results(
        self,
        result_sets: list[list[dict]],
        limit: int,
    ) -> list[dict]:
        """
        Merge multiple vector retrieval result sets.

        A chunk can be retrieved by both primary and
        secondary queries.

        Preserve:

            primary_score
            secondary_score
            best score
        """

        merged = {}

        for set_index, result_set in enumerate(
            result_sets
        ):

            is_secondary = (
                set_index > 0
            )

            for result in result_set:

                chunk = result.get(
                    "chunk"
                )

                if chunk is None:
                    continue

                chunk_id = getattr(
                    chunk,
                    "id",
                    None,
                )

                if chunk_id is None:
                    chunk_id = id(
                        chunk
                    )

                score = float(
                    result.get(
                        "score",
                        0.0,
                    )
                )

                existing = merged.get(
                    chunk_id
                )

                if existing is None:

                    merged[chunk_id] = {
                        "chunk": chunk,
                        "score": score,
                        "primary_score": (
                            0.0
                            if is_secondary
                            else score
                        ),
                        "secondary_score": (
                            score
                            if is_secondary
                            else 0.0
                        ),
                    }

                    continue

                # ------------------------------------------------
                # Preserve strongest score
                # ------------------------------------------------

                existing_score = float(
                    existing.get(
                        "score",
                        0.0,
                    )
                )

                if score > existing_score:
                    existing["score"] = score

                # ------------------------------------------------
                # Preserve query-specific scores
                # ------------------------------------------------

                if is_secondary:

                    existing[
                        "secondary_score"
                    ] = max(
                        float(
                            existing.get(
                                "secondary_score",
                                0.0,
                            )
                        ),
                        score,
                    )

                else:

                    existing[
                        "primary_score"
                    ] = max(
                        float(
                            existing.get(
                                "primary_score",
                                0.0,
                            )
                        ),
                        score,
                    )

        merged_results = list(
            merged.values()
        )

        merged_results.sort(
            key=lambda item: float(
                item.get(
                    "score",
                    0.0,
                )
            ),
            reverse=True,
        )

        return merged_results[:limit]

    # =======================================================
    # Final Relevance Threshold
    # =======================================================

    def _get_reranker_min_score(self) -> float:
        """
        Return the final reranker relevance threshold.

        IMPORTANT:

        RETRIEVAL_MIN_SCORE is the threshold used by
        vector retrieval.

        It should NOT automatically be reused for
        reranker scores because the two scoring systems
        have different distributions.

        If a dedicated setting exists, use it.

        Otherwise use 0.30 as a conservative default
        based on the current lexical reranker scale.
        """

        value = getattr(
            settings,
            "RERANKER_MIN_SCORE",
            0.30,
        )

        try:
            value = float(value)
        except (
            TypeError,
            ValueError,
        ):
            value = 0.30

        return max(
            0.0,
            min(
                1.0,
                value,
            ),
        )

    # =======================================================
    # Apply Final Relevance Gate
    # =======================================================

    def _apply_final_relevance_gate(
        self,
        results: list[dict],
        final_limit: int,
    ) -> list[dict]:
        """
        Apply the final relevance threshold AFTER reranking.

        This prevents weak keyword/vector candidates from
        entering the RAG context.

        Example:

            Rerank = 0.1114
            Threshold = 0.30

        Candidate is rejected.

        A useful result such as:

            Rerank = 0.6784

        is retained.
        """

        if not results:
            return []

        threshold = (
            self._get_reranker_min_score()
        )

        filtered_results = []

        for result in results:

            rerank_score = float(
                result.get(
                    "rerank_score",
                    result.get(
                        "score",
                        0.0,
                    ),
                )
            )

            if rerank_score >= threshold:

                filtered_results.append(
                    result
                )

        return filtered_results[
            :final_limit
        ]

    # =======================================================
    # Retrieve
    # =======================================================

    def retrieve(
        self,
        question: str,
        limit: int | None = None,
        history: list | None = None,
    ) -> list[dict]:
        """
        Retrieve relevant document chunks using:

        1. Conversation-aware semantic retrieval.
        2. Intent-focused semantic retrieval.
        3. Keyword retrieval.
        4. Candidate fusion.
        5. Hybrid scoring.
        6. Reranking.
        7. Final reranker relevance gate.
        """

        final_limit = (
            limit
            if limit is not None
            else settings.RETRIEVAL_LIMIT
        )

        candidate_limit = (
            settings.RETRIEVAL_CANDIDATE_LIMIT
        )

        # ---------------------------------------------------
        # Primary Query
        # ---------------------------------------------------

        retrieval_query = (
            self._build_retrieval_query(
                question=question,
                history=history,
            )
        )

        # ---------------------------------------------------
        # Secondary Query
        # ---------------------------------------------------

        secondary_query = (
            self._build_secondary_retrieval_query(
                question=question,
                history=history,
            )
        )

        # ===================================================
        # Vector Retrieval
        # ===================================================

        vector_result_sets = []

        primary_results = []

        if retrieval_query:

            primary_embedding = (
                self.embedding_service.generate_embedding(
                    retrieval_query
                )
            )

            primary_results = (
                self.chunk_repository.search_by_embedding(
                    embedding=primary_embedding,
                    limit=candidate_limit,
                    min_score=(
                        settings.RETRIEVAL_MIN_SCORE
                    ),
                )
            )

            vector_result_sets.append(
                primary_results
            )

        secondary_results = []

        if (
            secondary_query
            and secondary_query
            != retrieval_query
        ):

            secondary_embedding = (
                self.embedding_service.generate_embedding(
                    secondary_query
                )
            )

            secondary_results = (
                self.chunk_repository.search_by_embedding(
                    embedding=secondary_embedding,
                    limit=candidate_limit,
                    min_score=(
                        settings.RETRIEVAL_MIN_SCORE
                    ),
                )
            )

            vector_result_sets.append(
                secondary_results
            )

        # ---------------------------------------------------
        # Merge Both Vector Searches
        # ---------------------------------------------------

        vector_results = (
            self._merge_candidate_results(
                result_sets=vector_result_sets,
                limit=candidate_limit * 2,
            )
        )

        # ===================================================
        # Keyword Retrieval
        # ===================================================

        keyword_results = (
            self.chunk_repository.search_by_keyword(
                query=retrieval_query,
                limit=candidate_limit,
            )
        )

        # ===================================================
        # Hybrid Ranking
        # ===================================================

        results = self.hybrid_search.combine(
            vector_results=vector_results,
            keyword_results=keyword_results,
            limit=candidate_limit * 2,
        )

        # ===================================================
        # Reranking
        # ===================================================

        # IMPORTANT:
        #
        # Do NOT limit reranking directly to final_limit.
        #
        # We want the reranker to score the entire candidate
        # pool first. Then we apply the final relevance gate.
        #
        # Otherwise, weak candidates could occupy the top-K
        # slots before stronger candidates are considered.

        results = self.reranker.rerank(
            query=retrieval_query,
            candidates=results,
            limit=candidate_limit * 2,
        )

        # ===================================================
        # Final Relevance Gate
        # ===================================================

        results = (
            self._apply_final_relevance_gate(
                results=results,
                final_limit=final_limit,
            )
        )

        # ===================================================
        # Diagnostics
        # ===================================================

        self._log_retrieval_diagnostics(
            question=question,
            retrieval_query=retrieval_query,
            secondary_query=secondary_query,
            vector_results=vector_results,
            keyword_results=keyword_results,
            results=results,
            final_limit=final_limit,
            candidate_limit=candidate_limit,
        )

        return results

    # =======================================================
    # Diagnostics
    # =======================================================

    def _log_retrieval_diagnostics(
        self,
        question: str,
        retrieval_query: str,
        secondary_query: str,
        vector_results: list[dict],
        keyword_results: list[dict],
        results: list[dict],
        final_limit: int,
        candidate_limit: int,
    ) -> None:

        reranker_min_score = (
            self._get_reranker_min_score()
        )

        print()
        print("=" * 70)

        print(
            "HYBRID + MULTI-QUERY + RERANKER "
            "RETRIEVAL DIAGNOSTICS"
        )

        print("=" * 70)

        print(
            f"Question        : {question}"
        )

        print(
            f"Retrieval Query : {retrieval_query}"
        )

        if secondary_query:

            print(
                f"Secondary Query : {secondary_query}"
            )

        print(
            f"Candidate Limit : {candidate_limit}"
        )

        print(
            f"Final Limit     : {final_limit}"
        )

        print(
            f"Vector Min Score: "
            f"{settings.RETRIEVAL_MIN_SCORE}"
        )

        print(
            f"Reranker Min Score: "
            f"{reranker_min_score}"
        )

        print(
            f"Vector Candidates  : "
            f"{len(vector_results)}"
        )

        print(
            f"Keyword Candidates : "
            f"{len(keyword_results)}"
        )

        print(
            f"Final Results      : "
            f"{len(results)}"
        )

        print()
        print(
            "Final Reranked Results:"
        )

        if not results:

            print(
                "  No relevant results found."
            )

        else:

            for index, result in enumerate(
                results,
                start=1,
            ):

                chunk = result["chunk"]

                hybrid_score = float(
                    result.get(
                        "score",
                        0.0,
                    )
                )

                rerank_score = float(
                    result.get(
                        "rerank_score",
                        hybrid_score,
                    )
                )

                vector_score = float(
                    result.get(
                        "vector_score",
                        0.0,
                    )
                )

                keyword_score = float(
                    result.get(
                        "keyword_score",
                        0.0,
                    )
                )

                term_coverage = float(
                    result.get(
                        "term_coverage",
                        0.0,
                    )
                )

                phrase_score = float(
                    result.get(
                        "phrase_score",
                        0.0,
                    )
                )

                concept_score = float(
                    result.get(
                        "concept_score",
                        0.0,
                    )
                )

                definition_score = float(
                    result.get(
                        "definition_score",
                        0.0,
                    )
                )

                application_score = float(
                    result.get(
                        "application_score",
                        0.0,
                    )
                )

                comparison_score = float(
                    result.get(
                        "comparison_score",
                        0.0,
                    )
                )

                primary_score = float(
                    result.get(
                        "primary_score",
                        0.0,
                    )
                )

                secondary_score = float(
                    result.get(
                        "secondary_score",
                        0.0,
                    )
                )

                print(
                    f"  {index}. "
                    f"Chunk {chunk.chunk_index} "
                    f"| Hybrid: {hybrid_score:.4f} "
                    f"| Rerank: {rerank_score:.4f} "
                    f"| Vector: {vector_score:.4f} "
                    f"| Keyword: {keyword_score:.4f} "
                    f"| Primary: {primary_score:.4f} "
                    f"| Secondary: {secondary_score:.4f} "
                    f"| Coverage: {term_coverage:.4f} "
                    f"| Phrase: {phrase_score:.4f} "
                    f"| Concept: {concept_score:.4f} "
                    f"| Definition: {definition_score:.4f} "
                    f"| Application: {application_score:.4f} "
                    f"| Comparison: {comparison_score:.4f}"
                )

        print("=" * 70)
        print()