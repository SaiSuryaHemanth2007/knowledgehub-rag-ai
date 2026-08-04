class TXTProcessor:
    """
    Extracts text from plain text (.txt) documents.
    """

    def extract_text(self, file_path: str) -> str:
        """
        Extract all text from a TXT document.

        Args:
            file_path: Path to the TXT file.

        Returns:
            Document text.
        """

        with open(file_path, "r", encoding="utf-8") as file:
            return file.read().strip()