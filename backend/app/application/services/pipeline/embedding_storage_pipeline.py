from sqlalchemy.orm import Session

from app.application.services.pipeline.embedding_pipeline import (
    EmbeddingPipeline,
)
from app.domain.entities.chunk import Chunk
from app.infrastructure.repositories.chunk_repository import (
    ChunkRepository,
)


class EmbeddingStoragePipeline:
    """
    Filters low-quality chunks, generates embeddings,
    and stores them in PostgreSQL.
    """

    def __init__(
        self,
        db: Session,
    ):
        self.embedding_pipeline = EmbeddingPipeline()
        self.chunk_repository = ChunkRepository(db)

    def process(
        self,
        chunks: list[Chunk],
    ) -> None:
        """
        Filter chunks, generate embeddings,
        and store them in PostgreSQL.
        """

        if not chunks:
            return

        filtered_chunks = [
            chunk
            for chunk in chunks
            if (
                any(char.isalpha() for char in chunk.content)
                and len(chunk.content.strip()) >= 5
                and not chunk.content.strip().isdigit()
            )
        ]

        if not filtered_chunks:
            return

        texts = [
            chunk.content
            for chunk in filtered_chunks
        ]

        embeddings = self.embedding_pipeline.process(
            texts
        )

        self.chunk_repository.save_chunks(
            filtered_chunks,
            embeddings,
        )

        print("✓ Embeddings generated")
        print("✓ Chunks stored in PostgreSQL")