class ContextBuilder:
    """
    Builds the context string that will be sent
    to the language model.

    The original database chunk index is preserved
    so the language model can reference the same
    chunk that is displayed by the application.
    """

    def build(
        self,
        results: list[dict],
    ) -> str:
        """
        Build a context string from retrieved chunks.

        Each item in results contains:
        {
            "chunk": ChunkModel,
            "score": float,
        }
        """

        if not results:
            return ""

        context_parts = []

        for result in results:
            chunk = result["chunk"]
            score = result["score"]

            context_parts.append(
                f"[Chunk {chunk.chunk_index}]\n"
                f"Similarity: {score:.4f}\n"
                f"{chunk.content.strip()}"
            )

        return "\n\n".join(context_parts)