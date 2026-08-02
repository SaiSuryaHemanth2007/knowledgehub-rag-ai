from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.schemas.document import (
    DocumentCreate,
    DocumentResponse,
)
from app.application.use_cases.create_document import (
    CreateDocumentUseCase,
)
from app.domain.entities.document import Document
from app.infrastructure.repositories.document_repository import (
    DocumentRepository,
)

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post(
    "/",
    response_model=DocumentResponse,
    status_code=201,
)
def create_document(
    request: DocumentCreate,
    db: Session = Depends(get_db),
):
    repository = DocumentRepository(db)

    use_case = CreateDocumentUseCase(repository)

    document = Document(
        title=request.title,
        original_filename=request.original_filename,
        stored_filename=request.stored_filename,
        file_type=request.file_type,
        file_size=request.file_size,
    )

    return use_case.execute(document)