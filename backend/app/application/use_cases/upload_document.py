from fastapi import UploadFile

from app.application.services.document_processing.document_processor import (
    DocumentProcessor,
)
from app.application.services.file_storage import FileStorageService
from app.application.services.pipeline.document_processing_pipeline import (
    DocumentProcessingPipeline,
)
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
        self.document_processor = DocumentProcessor()
        self.pipeline = DocumentProcessingPipeline()

    def execute(
        self,
        title: str,
        file: UploadFile,
    ) -> Document:
        """
        Upload, extract text, generate chunks,
        and store document metadata.
        """

        # Save uploaded file
        saved_file = self.storage.save(file)

        # Extract text
        extracted_text = self.document_processor.extract_text(
            saved_file["path"]
        )

        # Create database record
        document = Document(
            title=title,
            original_filename=saved_file["original_filename"],
            stored_filename=saved_file["stored_filename"],
            file_type=saved_file["file_type"],
            file_size=saved_file["file_size"],
        )

        document = self.repository.create(document)

        # Generate chunks
        chunks = self.pipeline.process(
            document_id=document.id,
            extracted_text=extracted_text,
        )

        print("\n========== DOCUMENT SUMMARY ==========")
        print(f"Document ID : {document.id}")
        print(f"Chunks      : {len(chunks)}")

        if chunks:
            print("\nFirst Chunk:\n")
            print(chunks[0].content[:300])

        print("\n======================================\n")

        return document