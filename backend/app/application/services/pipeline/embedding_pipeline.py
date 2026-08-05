from typing import List

from app.application.services.embeddings.embedding_service import (
    EmbeddingService,
)


class EmbeddingPipeline:
    """
    Pipeline responsible for generating embeddings
    in configurable batches.
    """

    def __init__(
        self,
        batch_size: int = 20,
    ):
        self.batch_size = batch_size
        self.embedding_service = EmbeddingService()

    def process(
        self,
        texts: List[str],
    ) -> List[List[float]]:

        all_embeddings = []

        total = len(texts)

        for start in range(0, total, self.batch_size):

            end = min(start + self.batch_size, total)

            batch = texts[start:end]

            print(
                f"\nProcessing batch "
                f"{start // self.batch_size + 1} "
                f"({start + 1}-{end})"
            )

            embeddings = self.embedding_service.generate_embeddings(
                batch
            )

            all_embeddings.extend(embeddings)

        return all_embeddings