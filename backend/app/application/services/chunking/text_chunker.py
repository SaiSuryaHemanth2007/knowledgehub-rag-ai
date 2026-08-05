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

        while start < len(text):

            end = min(
                start + self.chunk_size,
                len(text),
            )

            # Try not to cut a word in half
            if end < len(text):
                while (
                    end > start
                    and not text[end].isspace()
                ):
                    end -= 1

                # If no whitespace was found,
                # fall back to the original size.
                if end == start:
                    end = min(
                        start + self.chunk_size,
                        len(text),
                    )

            chunk_content = text[start:end].strip()

            chunks.append(
                Chunk(
                    document_id=document_id,
                    chunk_index=chunk_index,
                    content=chunk_content,
                )
            )

            start = max(
                end - self.chunk_overlap,
                start + 1,
            )

            chunk_index += 1

        return chunks