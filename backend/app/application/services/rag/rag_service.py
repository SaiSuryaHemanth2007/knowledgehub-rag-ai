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

    def ask(
        self,
        question: str,
        limit: int = 5,
    ) -> dict:
        """
        Answer a question using the complete
        Retrieval-Augmented Generation pipeline.
        """

        # Retrieve relevant chunks
        results = self.retrieval_service.retrieve(
            question=question,
            limit=limit,
        )

        if not results:
            return {
                "answer": (
                    "I couldn't find any relevant information "
                    "in the uploaded documents."
                ),
                "sources": [],
            }

        # Build context
        context = self.context_builder.build(results)

        # Build prompts
        system_prompt, user_prompt = (
            self.prompt_builder.build(
                context=context,
                question=question,
            )
        )

        # Generate answer
        answer = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
        )

        # Build source metadata
        sources = []

        for result in results:

            chunk = result["chunk"]

            sources.append(
                {
                    "document_id": chunk.document_id,
                    "document_title": chunk.document.title,
                    "original_filename": chunk.document.original_filename,
                    "chunk_index": chunk.chunk_index,
                    "score": result["score"],
                    "preview": (
                        chunk.content[:180]
                        .replace("\n", " ")
                        .strip()
                        + "..."
                    ),
                }
            )

        return {
            "answer": answer,
            "sources": sources,
        }