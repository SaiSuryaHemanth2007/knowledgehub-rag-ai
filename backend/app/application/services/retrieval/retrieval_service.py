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
        Retrieval Query
            ↓
        Query Embedding
            ↓
        ┌───────────────────────────────┐
        │                               │
        ↓                               ↓
    Vector Search                  Keyword Search
        ↓                               ↓
    Candidates                    Candidates
        └───────────────┬───────────────┘
                        ↓
                  Hybrid Scoring
                        ↓
                    Reranker
                        ↓
                    Final Top K
                        ↓
                  ContextBuilder
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

        Normal question:

            What is generative AI?

        Follow-up question:

            Previous:
                What is generative AI?

            Current:
                What are its main applications?

        Becomes:

            Topic: What is generative AI?
            Intent: applications, use cases, examples,
                     business functions
            Question: What are its main applications?

        Conversation history is used only when a
        previous user question exists.
        """

        question = (
            question or ""
        ).strip()

        if not question:
            return ""

        # ---------------------------------------------------
        # No history
        # ---------------------------------------------------

        if not history:
            return question

        # ---------------------------------------------------
        # Keep recent messages only
        # ---------------------------------------------------

        recent_history = history[-6:]

        user_messages = []

        for message in recent_history:

            # ------------------------------------------------
            # Dictionary message
            # ------------------------------------------------

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

            # ------------------------------------------------
            # SQLAlchemy MessageModel
            # ------------------------------------------------

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

            # ------------------------------------------------
            # Only previous user questions are needed
            # as the main topic signal.
            # ------------------------------------------------

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

        # ---------------------------------------------------
        # No usable user history
        # ---------------------------------------------------

        if not user_messages:
            return question

        # ---------------------------------------------------
        # Need a previous question to establish the topic.
        #
        # The current question is normally not included
        # in history because chat.py loads history before
        # saving the current question.
        #
        # But this also safely handles cases where it is.
        # ---------------------------------------------------

        previous_question = user_messages[-1]

        # ---------------------------------------------------
        # Detect generic follow-up intent
        # ---------------------------------------------------

        intent_terms = (
            self._expand_follow_up_query(
                question
            )
        )

        # ---------------------------------------------------
        # If the question is not a recognized follow-up,
        # preserve the existing conversation-aware behavior.
        # ---------------------------------------------------

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

        # ---------------------------------------------------
        # Focused follow-up retrieval query
        # ---------------------------------------------------

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

        This is intentionally generic and does not
        contain document-specific terminology.

        Examples:

            What are its main applications?

                →
            applications, use cases, examples,
            business functions

            What are its benefits?

                →
            benefits, advantages, value, impact

            Give me examples.

                →
            examples, use cases, practical examples
        """

        normalized = (
            question or ""
        ).lower().strip()

        if not normalized:
            return ""

        # ===================================================
        # Applications / Use Cases
        # ===================================================

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

        # ===================================================
        # Benefits / Advantages
        # ===================================================

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

        # ===================================================
        # Examples
        # ===================================================

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

        # ===================================================
        # Features / Capabilities
        # ===================================================

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

        # ===================================================
        # Comparison
        # ===================================================

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

        # ===================================================
        # Definition / Explanation
        # ===================================================

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
    # Retrieve
    # =======================================================

    def retrieve(
        self,
        question: str,
        limit: int | None = None,
        history: list | None = None,
    ) -> list[dict]:
        """
        Retrieve relevant document chunks using
        hybrid retrieval followed by reranking.

        Two independent retrieval strategies are used:

        1. Vector semantic search.
        2. PostgreSQL keyword search.

        Both retrieve a larger candidate pool.

        The candidates are then combined using
        HybridSearchService.

        The hybrid results are passed to the reranker.

        Finally, only the configured number of
        top results are returned.
        """

        # ---------------------------------------------------
        # Final result limit
        # ---------------------------------------------------

        final_limit = (
            limit
            if limit is not None
            else settings.RETRIEVAL_LIMIT
        )

        # ---------------------------------------------------
        # Candidate limit
        # ---------------------------------------------------

        candidate_limit = (
            settings.RETRIEVAL_CANDIDATE_LIMIT
        )

        # ---------------------------------------------------
        # Build retrieval query
        # ---------------------------------------------------

        retrieval_query = (
            self._build_retrieval_query(
                question=question,
                history=history,
            )
        )

        # ---------------------------------------------------
        # Generate embedding
        # ---------------------------------------------------

        query_embedding = (
            self.embedding_service.generate_embedding(
                retrieval_query
            )
        )

        # ===================================================
        # Vector Candidate Search
        # ===================================================

        vector_results = (
            self.chunk_repository.search_by_embedding(
                embedding=query_embedding,
                limit=candidate_limit,
                min_score=settings.RETRIEVAL_MIN_SCORE,
            )
        )

        # ===================================================
        # Keyword Candidate Search
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
            limit=candidate_limit,
        )

        # ===================================================
        # Reranking
        # ===================================================

        results = self.reranker.rerank(
            query=retrieval_query,
            candidates=results,
            limit=final_limit,
        )

        # ===================================================
        # Diagnostics
        # ===================================================

        self._log_retrieval_diagnostics(
            question=question,
            retrieval_query=retrieval_query,
            vector_results=vector_results,
            keyword_results=keyword_results,
            results=results,
            final_limit=final_limit,
            candidate_limit=candidate_limit,
        )

        return results

    # =======================================================
    # Retrieval Diagnostics
    # =======================================================

    def _log_retrieval_diagnostics(
        self,
        question: str,
        retrieval_query: str,
        vector_results: list[dict],
        keyword_results: list[dict],
        results: list[dict],
        final_limit: int,
        candidate_limit: int,
    ) -> None:
        """
        Log retrieval information for debugging
        and evaluation.

        Displays:

        - Hybrid score
        - Final rerank score
        - Vector score
        - Keyword score
        - Query term coverage
        - Phrase relevance
        - Concept score
        - Definition score
        """

        print()
        print("=" * 70)

        print(
            "HYBRID + RERANKER RETRIEVAL DIAGNOSTICS"
        )

        print("=" * 70)

        print(
            f"Question        : {question}"
        )

        print(
            f"Retrieval Query : {retrieval_query}"
        )

        print(
            f"Candidate Limit : {candidate_limit}"
        )

        print(
            f"Final Limit     : {final_limit}"
        )

        print(
            f"Min Score       : "
            f"{settings.RETRIEVAL_MIN_SCORE}"
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

                print(
                    f"  {index}. "
                    f"Chunk {chunk.chunk_index} "
                    f"| Hybrid: {hybrid_score:.4f} "
                    f"| Rerank: {rerank_score:.4f} "
                    f"| Vector: {vector_score:.4f} "
                    f"| Keyword: {keyword_score:.4f} "
                    f"| Coverage: {term_coverage:.4f} "
                    f"| Phrase: {phrase_score:.4f} "
                    f"| Concept: {concept_score:.4f} "
                    f"| Definition: {definition_score:.4f}"
                )

        print("=" * 70)
        print()