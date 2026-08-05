from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.application.services.document_processing.document_processor import (
    DocumentProcessor,
)
from app.application.services.file_storage import FileStorageService
from app.application.services.pipeline.document_processing_pipeline import (
    DocumentProcessingPipeline,
)
from app.application.services.pipeline.embedding_storage_pipeline import (
    EmbeddingStoragePipeline,
)
from app.domain.entities.document import Document
from app.infrastructure.repositories.document_repository import (
    DocumentRepository,
)


class UploadDocumentUseCase:
    """
    Handles the complete document ingestion pipeline.
    """

    def __init__(
        self,
        repository: DocumentRepository,
        storage: FileStorageService,
        db: Session,
    ):
        self.repository = repository
        self.storage = storage
        self.document_processor = DocumentProcessor()
        self.processing_pipeline = DocumentProcessingPipeline()
        self.embedding_storage_pipeline = EmbeddingStoragePipeline(db)

    def execute(
        self,
        title: str,
        file: UploadFile,
    ) -> Document:
        """
        Upload, process, embed, and store a document.
        """

        # Save uploaded file
        saved_file = self.storage.save(file)

        # Extract text
        extracted_text = self.document_processor.extract_text(
            saved_file["path"]
        )

        # Create document
        document = Document(
            title=title,
            original_filename=saved_file["original_filename"],
            stored_filename=saved_file["stored_filename"],
            file_type=saved_file["file_type"],
            file_size=saved_file["file_size"],
        )

        document = self.repository.create(document)

        # Chunk document
        chunks = self.processing_pipeline.process(
            document_id=document.id,
            extracted_text=extracted_text,
        )

        print("\n========== DOCUMENT SUMMARY ==========")
        print(f"Document ID : {document.id}")
        print(f"Chunks      : {len(chunks)}")

        # Generate embeddings and store
        self.embedding_storage_pipeline.process(chunks)

        print("✓ Embeddings stored successfully")
        print("======================================\n")

        return document