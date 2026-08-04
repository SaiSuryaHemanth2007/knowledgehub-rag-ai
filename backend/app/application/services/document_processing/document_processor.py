from pathlib import Path

from app.application.services.document_processing.docx_processor import (
    DOCXProcessor,
)
from app.application.services.document_processing.pdf_processor import (
    PDFProcessor,
)
from app.application.services.document_processing.txt_processor import (
    TXTProcessor,
)


class DocumentProcessor:
    """
    Selects the correct processor based on the document type.
    """

    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.docx_processor = DOCXProcessor()
        self.txt_processor = TXTProcessor()

    def extract_text(self, file_path: str) -> str:
        """
        Extract text from a supported document.
        """

        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return self.pdf_processor.extract_text(file_path)

        if extension == ".docx":
            return self.docx_processor.extract_text(file_path)

        if extension == ".txt":
            return self.txt_processor.extract_text(file_path)

        raise ValueError(
            f"Unsupported file type: {extension}"
        )