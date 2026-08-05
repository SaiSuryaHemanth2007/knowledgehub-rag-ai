class ContextBuilder:
    """
    Builds the context string that will be sent
    to the language model.
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

        for i, result in enumerate(results, start=1):
            chunk = result["chunk"]

            context_parts.append(
                f"[Chunk {i}]\n{chunk.content.strip()}"
            )

        return "\n\n".join(context_parts)