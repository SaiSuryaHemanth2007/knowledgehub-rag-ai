from sqlalchemy.orm import Session

from app.domain.entities.document import Document
from app.infrastructure.database.models.document import DocumentModel


class DocumentRepository:
    """
    Repository responsible for persisting Document entities.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        document: Document,
    ) -> Document:
        """
        Save a document and return the domain entity
        populated with generated fields.
        """

        model = DocumentModel(
            title=document.title,
            original_filename=document.original_filename,
            stored_filename=document.stored_filename,
            file_type=document.file_type,
            file_size=document.file_size,
            status=document.status,
        )

        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return Document(
            id=model.id,
            title=model.title,
            original_filename=model.original_filename,
            stored_filename=model.stored_filename,
            file_type=model.file_type,
            file_size=model.file_size,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def get_by_id(
        self,
        document_id: int,
    ) -> Document | None:

        model = (
            self.db.query(DocumentModel)
            .filter(DocumentModel.id == document_id)
            .first()
        )

        if model is None:
            return None

        return Document(
            id=model.id,
            title=model.title,
            original_filename=model.original_filename,
            stored_filename=model.stored_filename,
            file_type=model.file_type,
            file_size=model.file_size,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def get_all(
        self,
    ) -> list[Document]:

        models = self.db.query(DocumentModel).all()

        return [
            Document(
                id=model.id,
                title=model.title,
                original_filename=model.original_filename,
                stored_filename=model.stored_filename,
                file_type=model.file_type,
                file_size=model.file_size,
                status=model.status,
                created_at=model.created_at,
                updated_at=model.updated_at,
            )
            for model in models
        ]

    def delete(
        self,
        document_id: int,
    ) -> None:

        (
            self.db.query(DocumentModel)
            .filter(DocumentModel.id == document_id)
            .delete()
        )

        self.db.commit()