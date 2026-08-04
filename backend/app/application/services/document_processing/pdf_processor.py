import fitz


class PDFProcessor:
    """
    Extracts text from PDF documents.
    """

    def extract_text(self, file_path: str) -> str:
        """
        Extract all text from a PDF.

        Args:
            file_path: Path to the PDF file.

        Returns:
            Extracted text as a single string.
        """

        with fitz.open(file_path) as document:
            text = ""

            for page in document:
                text += page.get_text()

        return text.strip()