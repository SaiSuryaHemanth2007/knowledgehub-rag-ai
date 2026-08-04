from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


class FileStorageService:
    """
    Handles storing uploaded files.
    """

    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        file: UploadFile,
    ) -> dict:
        """
        Save an uploaded file.

        Returns:
            Dictionary containing file metadata.
        """

        extension = Path(file.filename).suffix.lower()

        stored_filename = f"{uuid4()}{extension}"

        destination = self.upload_dir / stored_filename

        content = file.file.read()

        destination.write_bytes(content)

        return {
            "path": str(destination),
            "original_filename": file.filename,
            "stored_filename": stored_filename,
            "file_type": file.content_type,
            "file_size": len(content),
        }