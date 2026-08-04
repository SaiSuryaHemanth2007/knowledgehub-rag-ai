from docx import Document


class DOCXProcessor:
    """
    Extracts text from Microsoft Word (.docx) documents.
    """

    def extract_text(self, file_path: str) -> str:
        """
        Extract all text from a DOCX document.

        Args:
            file_path: Path to the DOCX file.

        Returns:
            Extracted text as a single string.
        """

        document = Document(file_path)

        text = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                text.append(paragraph.text)

        return "\n".join(text)