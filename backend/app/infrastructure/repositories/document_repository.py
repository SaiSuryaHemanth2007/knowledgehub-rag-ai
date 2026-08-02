from sqlalchemy.orm import Session

from app.domain.entities.document import Document
from app.infrastructure.repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository[Document]):
    """
    Repository responsible for Document persistence.
    """

    def __init__(self, db: Session):
        super().__init__(db, Document)