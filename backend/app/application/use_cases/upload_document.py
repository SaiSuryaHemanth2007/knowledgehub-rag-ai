from fastapi import UploadFile

from app.application.services.document_processing.document_processor import (
    DocumentProcessor,
)
from app.application.services.file_storage import FileStorageService
from app.domain.entities.document import Document
from app.infrastructure.repositories.document_repository import (
    DocumentRepository,
)


class UploadDocumentUseCase:
    """
    Handles uploading and processing documents.
    """

    def __init__(
        self,
        repository: DocumentRepository,
        storage: FileStorageService,
    ):
        self.repository = repository
        self.storage = storage
        self.processor = DocumentProcessor()

    def execute(
        self,
        title: str,
        file: UploadFile,
    ) -> Document:
        """
        Upload a document, extract its text,
        and store its metadata.
        """

        # Save uploaded file
        saved_file = self.storage.save(file)

        # Extract document text
        extracted_text = self.processor.extract_text(
            saved_file["path"]
        )

        # Temporary verification
        print("\n========== EXTRACTED TEXT ==========\n")
        print(extracted_text[:500])
        print("\n====================================\n")

        # Create database entity
        document = Document(
            title=title,
            original_filename=saved_file["original_filename"],
            stored_filename=saved_file["stored_filename"],
            file_type=saved_file["file_type"],
            file_size=saved_file["file_size"],
        )

        return self.repository.create(document)