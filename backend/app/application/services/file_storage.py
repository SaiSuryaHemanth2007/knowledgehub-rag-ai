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

    def save_file(
        self,
        file: UploadFile,
    ) -> tuple[str, str, int]:
        """
        Saves an uploaded file to disk.

        Returns:
            tuple:
                stored_filename,
                content_type,
                file_size
        """

        # Get the original file extension (.pdf, .docx, etc.)
        extension = Path(file.filename).suffix

        # Generate a unique filename
        stored_filename = f"{uuid4()}{extension}"
        destination = self.upload_dir / stored_filename
        content = file.file.read()
        destination.write_bytes(content)

        return (
            stored_filename,
            file.content_type,
            len(content),
        )