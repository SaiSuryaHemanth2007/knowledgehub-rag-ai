from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

from app.domain.entities.chunk import Chunk
from app.infrastructure.database.models.chunk import ChunkModel


class ChunkRepository:
    """
    Repository responsible for storing and retrieving
    document chunks.
    """

    def __init__(self, db: Session):
        self.db = db

    # =======================================================
    # Save Chunks
    # =======================================================

    def save_chunks(
        self,
        chunks: list[Chunk],
        embeddings: list[list[float]],
    ) -> None:
        """
        Store chunks together with their embeddings.
        """

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

    # =======================================================
    # Semantic / Vector Search
    # =======================================================

    def search_by_embedding(
        self,
        embedding: list[float],
        limit: int = 5,
        min_score: float = 0.0,
    ) -> list[dict]:
        """
        Perform semantic similarity search using pgvector.

        Results are ordered by cosine similarity and filtered
        using a minimum similarity score.
        """

        distance_expression = (
            ChunkModel.embedding.cosine_distance(
                embedding
            )
        )

        results = (
            self.db.query(
                ChunkModel,
                distance_expression.label(
                    "distance"
                ),
            )
            .options(
                joinedload(
                    ChunkModel.document
                )
            )
            .order_by(
                distance_expression
            )
            .limit(limit)
            .all()
        )

        filtered_results = []

        for chunk, distance in results:

            score = round(
                1 - distance,
                4,
            )

            if score < min_score:
                continue

            filtered_results.append(
                {
                    "chunk": chunk,
                    "score": score,
                }
            )

        return filtered_results

    # =======================================================
    # Keyword Search
    # =======================================================

    def search_by_keyword(
        self,
        query: str,
        limit: int = 5,
    ) -> list[dict]:
        """
        Perform PostgreSQL full-text keyword search.

        This search complements vector search by finding
        chunks containing terms that are directly related
        to the user's query.

        Returns:
            [
                {
                    "chunk": ChunkModel,
                    "score": float,
                }
            ]
        """

        if not query.strip():
            return []

        search_vector = func.to_tsvector(
            "english",
            ChunkModel.content,
        )

        search_query = func.websearch_to_tsquery(
            "english",
            query,
        )

        rank_expression = func.ts_rank(
            search_vector,
            search_query,
        )

        results = (
            self.db.query(
                ChunkModel,
                rank_expression.label(
                    "rank"
                ),
            )
            .options(
                joinedload(
                    ChunkModel.document
                )
            )
            .filter(
                search_vector.op("@@")(
                    search_query
                )
            )
            .order_by(
                rank_expression.desc()
            )
            .limit(limit)
            .all()
        )

        return [
            {
                "chunk": chunk,
                "score": round(
                    float(rank),
                    4,
                ),
            }
            for chunk, rank in results
        ]

    # =======================================================
    # Get Chunks By Document
    # =======================================================

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

    # =======================================================
    # Delete Chunks By Document
    # =======================================================

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