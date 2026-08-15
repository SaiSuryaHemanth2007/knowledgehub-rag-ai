from sqlalchemy.orm import Session

from app.application.services.embeddings.embedding_service import (
    EmbeddingService,
)
from app.infrastructure.repositories.chunk_repository import (
    ChunkRepository,
)


class RetrievalService:
    """
    Generates an embedding for a conversation-aware user query
    and retrieves the most relevant document chunks together
    with their similarity scores.

    The retrieval query includes recent conversation history so
    follow-up questions such as:

        "What layer does it operate on?"

    can be understood in context.
    """

    def __init__(self, db: Session):

        self.embedding_service = EmbeddingService()

        self.chunk_repository = ChunkRepository(db)

    # =======================================================
    # Build Conversation-Aware Retrieval Query
    # =======================================================

    def _build_retrieval_query(
        self,
        question: str,
        history: list | None = None,
    ) -> str:
        """
        Build a retrieval query using the current question
        and recent conversation history.

        This is intentionally done before embedding so that
        semantic search can understand follow-up questions.
        """

        if not history:

            return question

        history_lines = []

        # ---------------------------------------------------
        # Use only recent messages.
        #
        # This prevents very old conversation messages from
        # dominating the embedding.
        # ---------------------------------------------------

        recent_history = history[-4:]

        for message in recent_history:

            role = getattr(
                message,
                "role",
                "unknown",
            )

            content = getattr(
                message,
                "content",
                "",
            )

            if not content:
                continue

            history_lines.append(
                f"{role.capitalize()}: {content}"
            )

        if not history_lines:

            return question

        history_text = "\n".join(
            history_lines
        )

        return f"""
Previous conversation:

{history_text}

Current question:

{question}
""".strip()

    # =======================================================
    # Retrieve
    # =======================================================

    def retrieve(
        self,
        question: str,
        limit: int = 5,
        history: list | None = None,
    ) -> list[dict]:
        """
        Retrieve the most semantically relevant chunks.

        Conversation history is included when generating the
        retrieval embedding so that follow-up questions can
        retrieve the correct document chunks.

        Returns:
            [
                {
                    "chunk": ChunkModel,
                    "score": float,
                }
            ]
        """

        # ---------------------------------------------------
        # Build context-aware query
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

        # ---------------------------------------------------
        # Vector similarity search
        # ---------------------------------------------------

        return self.chunk_repository.search_by_embedding(
            embedding=query_embedding,
            limit=limit,
        )