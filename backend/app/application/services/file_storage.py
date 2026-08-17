from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


class FileStorageService:
    """
    Handles storing and deleting uploaded files.
    """

    def __init__(
        self,
        upload_dir: str = "uploads",
    ):
        self.upload_dir = Path(upload_dir)

        self.upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    # =====================================================
    # Save File
    # =====================================================

    def save(
        self,
        file: UploadFile,
    ) -> dict:
        """
        Save an uploaded file.

        Returns:
            Dictionary containing file metadata.
        """

        extension = Path(
            file.filename
        ).suffix.lower()

        stored_filename = (
            f"{uuid4()}{extension}"
        )

        destination = (
            self.upload_dir /
            stored_filename
        )

        content = file.file.read()

        destination.write_bytes(
            content
        )

        return {
            "path": str(destination),
            "original_filename": file.filename,
            "stored_filename": stored_filename,
            "file_type": file.content_type,
            "file_size": len(content),
        }

    # =====================================================
    # Delete File
    # =====================================================

    def delete(
        self,
        stored_filename: str,
    ) -> bool:
        """
        Delete an uploaded file.

        Returns:
            True if the file was deleted.
            False if the file does not exist.
        """

        file_path = (
            self.upload_dir /
            stored_filename
        )

        if not file_path.exists():
            return False

        file_path.unlink()

        return True