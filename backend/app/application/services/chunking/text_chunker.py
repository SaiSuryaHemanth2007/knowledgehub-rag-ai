from app.domain.entities.chunk import Chunk


class TextChunker:
    """
    Splits extracted document text into overlapping chunks.
    """

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(
        self,
        document_id: int,
        text: str,
    ) -> list[Chunk]:
        """
        Split text into overlapping chunks while trying
        to preserve whole words.
        """

        chunks = []

        start = 0
        chunk_index = 0
        text_length = len(text)

        while start < text_length:

            end = min(
                start + self.chunk_size,
                text_length,
            )

            # Try not to cut a word in half
            if end < text_length:

                while (
                    end > start
                    and not text[end].isspace()
                ):
                    end -= 1

                if end == start:
                    end = min(
                        start + self.chunk_size,
                        text_length,
                    )

            chunk_content = text[start:end].strip()

            # Skip completely empty chunks
            if chunk_content:
                chunks.append(
                    Chunk(
                        document_id=document_id,
                        chunk_index=chunk_index,
                        content=chunk_content,
                    )
                )
                chunk_index += 1

            # Stop once we've reached the end
            if end >= text_length:
                break

            start = end - self.chunk_overlap

        return chunks