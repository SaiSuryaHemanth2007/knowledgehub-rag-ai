from sqlalchemy.orm import Session

from app.application.services.embeddings.embedding_service import (
    EmbeddingService,
)
from app.infrastructure.database.models.chunk import ChunkModel
from app.infrastructure.repositories.chunk_repository import (
    ChunkRepository,
)


class RetrievalService:
    """
    Generates an embedding for a user query and retrieves
    the most relevant document chunks.
    """

    def __init__(self, db: Session):
        self.embedding_service = EmbeddingService()
        self.chunk_repository = ChunkRepository(db)

    def retrieve(
        self,
        question: str,
        limit: int = 5,
    ) -> list[ChunkModel]:
        """
        Retrieve the most semantically relevant chunks.
        """

        query_embedding = self.embedding_service.generate_embedding(
            question
        )

        return self.chunk_repository.search_by_embedding(
            embedding=query_embedding,
            limit=limit,
        )