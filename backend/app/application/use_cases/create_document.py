from app.domain.entities.document import Document
from app.infrastructure.repositories.document_repository import (
    DocumentRepository,
)


class CreateDocumentUseCase:
    """
    Handles the business logic for creating a document.
    """

    def __init__(self, repository: DocumentRepository):
        self.repository = repository

    def execute(self, document: Document) -> Document:
        """
        Execute the create document use case.
        """
        return self.repository.create(document)