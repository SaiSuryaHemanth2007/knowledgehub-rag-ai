from app.application.services.chunking.text_chunker import TextChunker
from app.domain.entities.chunk import Chunk


class DocumentProcessingPipeline:
    """
    Handles document text processing after extraction.
    """

    def __init__(self):
        self.chunker = TextChunker()

    def process(
        self,
        document_id: int,
        extracted_text: str,
    ) -> list[Chunk]:
        """
        Convert extracted text into chunks.
        """

        return self.chunker.chunk_text(
            document_id=document_id,
            text=extracted_text,
        )