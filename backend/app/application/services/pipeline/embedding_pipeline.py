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
        texts: list[str],
    ) -> list[list[float]]:
        """
        Process all texts by splitting them into batches
        and generating embeddings.
        """

        all_embeddings = []

        total = len(texts)

        total_batches = (
            total + self.batch_size - 1
        ) // self.batch_size

        for start in range(0, total, self.batch_size):

            end = min(
                start + self.batch_size,
                total,
            )

            batch = texts[start:end]

            batch_number = (
                start // self.batch_size
            ) + 1

            print()
            print("=" * 60)
            print(
                f"Processing Batch {batch_number}/{total_batches}"
            )
            print(
                f"Chunks: {start + 1} - {end}"
            )
            print("=" * 60)

            embeddings = (
                self.embedding_service.generate_embeddings(
                    batch
                )
            )

            all_embeddings.extend(
                embeddings
            )

            print(
                f"✓ Batch {batch_number} Completed"
            )

        return all_embeddings