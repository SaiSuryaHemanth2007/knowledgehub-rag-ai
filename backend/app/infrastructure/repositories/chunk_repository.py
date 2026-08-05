from sqlalchemy.orm import Session

from app.domain.entities.chunk import Chunk
from app.infrastructure.database.models.chunk import ChunkModel


class ChunkRepository:
    """
    Repository responsible for storing and retrieving
    document chunks.
    """

    def __init__(self, db: Session):
        self.db = db

    def save_chunks(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ) -> None:

        chunk_models = []

        for chunk, embedding in zip(chunks, embeddings):
            chunk_models.append(
                ChunkModel(
                    document_id=chunk.document_id,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    embedding=embedding,
                )
            )

        self.db.add_all(chunk_models)
        self.db.commit()

    def search_by_embedding(
        self,
        embedding: list[float],
        limit: int = 5,
    ) -> list[ChunkModel]:
        """
        Perform semantic similarity search using pgvector ORM.
        """

        return (
            self.db.query(ChunkModel)
            .order_by(
                ChunkModel.embedding.cosine_distance(
                    embedding
                )
            )
            .limit(limit)
            .all()
        )

    def get_by_document(
        self,
        document_id: int,
    ) -> list[ChunkModel]:

        return (
            self.db.query(ChunkModel)
            .filter(
                ChunkModel.document_id == document_id
            )
            .order_by(
                ChunkModel.chunk_index
            )
            .all()
        )

    def delete_by_document(
        self,
        document_id: int,
    ) -> None:

        (
            self.db.query(ChunkModel)
            .filter(
                ChunkModel.document_id == document_id
            )
            .delete()
        )

        self.db.commit()