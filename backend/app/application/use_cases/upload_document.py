from fastapi import UploadFile

from app.application.services.file_storage import FileStorageService
from app.domain.entities.document import Document
from app.infrastructure.repositories.document_repository import (
    DocumentRepository,
)


class UploadDocumentUseCase:
    """
    Uploads a document and stores both
    the physical file and its metadata.
    """

    def __init__(
        self,
        repository: DocumentRepository,
        storage: FileStorageService,
    ):
        self.repository = repository
        self.storage = storage

    def execute(
        self,
        title: str,
        file: UploadFile,
    ) -> Document:
        """
        Upload a document.

        Steps:
        1. Save file to disk
        2. Create Document entity
        3. Save metadata to database
        4. Return saved document
        """

        stored_filename, file_type, file_size = (
            self.storage.save_file(file)
        )

        document = Document(
            title=title,
            original_filename=file.filename,
            stored_filename=stored_filename,
            file_type=file_type,
            file_size=file_size,
        )

        return self.repository.create(document)