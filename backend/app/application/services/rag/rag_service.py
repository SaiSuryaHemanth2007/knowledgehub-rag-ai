from typing import Generator

from sqlalchemy.orm import Session

from app.application.services.llm.groq_service import GroqService
from app.application.services.rag.context_builder import ContextBuilder
from app.application.services.rag.prompt_builder import PromptBuilder
from app.application.services.retrieval.retrieval_service import (
    RetrievalService,
)


class RAGService:
    """
    End-to-end Retrieval-Augmented Generation service.

    Pipeline:

        Question
            ↓
        Conversation History
            ↓
        Conversation-Aware Retrieval
            ↓
        RetrievalService
            ↓
        ContextBuilder
            ↓
        PromptBuilder
            ↓
        GroqService
            ↓
        Final Answer + Sources
    """

    def __init__(
        self,
        db: Session,
    ):
        self.retrieval_service = RetrievalService(db)
        self.context_builder = ContextBuilder()
        self.prompt_builder = PromptBuilder()
        self.llm = GroqService()

    # =======================================================
    # Normal RAG
    # =======================================================

    def ask(
        self,
        question: str,
        limit: int = 5,
        history: list | None = None,
    ) -> dict:
        """
        Answer a question using Retrieval-Augmented Generation
        and optional conversation history.
        """

        # ---------------------------------------------------
        # Normalize conversation history
        # ---------------------------------------------------

        conversation_history = (
            history if history is not None else []
        )

        # ---------------------------------------------------
        # Retrieve relevant document chunks
        #
        # Conversation history is passed to retrieval so
        # follow-up questions can be understood in context.
        # ---------------------------------------------------

        results = self.retrieval_service.retrieve(
            question=question,
            limit=limit,
            history=conversation_history,
        )

        # ---------------------------------------------------
        # No relevant documents
        # ---------------------------------------------------

        if not results:
            return {
                "answer": (
                    "I couldn't find any relevant information "
                    "in the uploaded documents."
                ),
                "sources": [],
            }

        # ---------------------------------------------------
        # Build document context
        # ---------------------------------------------------

        context = self.context_builder.build(
            results
        )

        # ---------------------------------------------------
        # Build prompts
        # ---------------------------------------------------

        system_prompt, user_prompt = (
            self.prompt_builder.build(
                context=context,
                question=question,
                history=conversation_history,
            )
        )

        # ---------------------------------------------------
        # Generate complete answer
        # ---------------------------------------------------

        answer = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        # ---------------------------------------------------
        # Build source metadata
        # ---------------------------------------------------

        sources = self._build_sources(
            results
        )

        return {
            "answer": answer,
            "sources": sources,
        }

    # =======================================================
    # Streaming RAG
    # =======================================================

    def stream_ask(
        self,
        question: str,
        conversation_history: list | None = None,
        limit: int = 5,
    ) -> tuple[
        Generator[str, None, None],
        list,
    ]:
        """
        Stream an answer token-by-token using
        Retrieval-Augmented Generation and
        conversation history.

        Conversation history is used during retrieval
        so follow-up questions can retrieve the
        correct document chunks.

        Returns:

            token_stream:
                Generator yielding answer chunks.

            sources:
                Retrieved document source metadata.
        """

        # ---------------------------------------------------
        # Normalize conversation history
        # ---------------------------------------------------

        if conversation_history is None:
            conversation_history = []

        # ---------------------------------------------------
        # Retrieve relevant document chunks
        #
        # IMPORTANT:
        # Pass conversation history into retrieval.
        # ---------------------------------------------------

        results = self.retrieval_service.retrieve(
            question=question,
            limit=limit,
            history=conversation_history,
        )

        # ---------------------------------------------------
        # No relevant documents
        # ---------------------------------------------------

        if not results:

            def fallback_stream():
                yield (
                    "I couldn't find any relevant information "
                    "in the uploaded documents."
                )

            return fallback_stream(), []

        # ---------------------------------------------------
        # Build document context
        # ---------------------------------------------------

        context = self.context_builder.build(
            results
        )

        # ---------------------------------------------------
        # Build prompts
        # ---------------------------------------------------

        system_prompt, user_prompt = (
            self.prompt_builder.build(
                context=context,
                question=question,
                history=conversation_history,
            )
        )

        # ---------------------------------------------------
        # Build source metadata
        # ---------------------------------------------------

        sources = self._build_sources(
            results
        )

        # ---------------------------------------------------
        # Start Groq streaming
        # ---------------------------------------------------

        token_stream = self.llm.stream_generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        return token_stream, sources

    # =======================================================
    # Source Metadata
    # =======================================================

    def _build_sources(
        self,
        results: list,
    ) -> list:
        """
        Convert retrieval results into
        frontend-friendly source metadata.
        """

        sources = []

        for result in results:

            chunk = result["chunk"]

            sources.append(
                {
                    "document_id": chunk.document_id,

                    "document_title": (
                        chunk.document.title
                    ),

                    "original_filename": (
                        chunk.document.original_filename
                    ),

                    "chunk_index": (
                        chunk.chunk_index
                    ),

                    "score": result.get("rerank_score", result["score"]),

                    "preview": (
                        chunk.content[:180]
                        .replace("\n", " ")
                        .strip()
                        + "..."
                    ),
                }
            )

        return sources