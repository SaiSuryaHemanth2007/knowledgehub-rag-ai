from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlalchemy.orm import Session

from app.application.services.file_storage import FileStorageService
from app.application.use_cases.upload_document import UploadDocumentUseCase
from app.domain.entities.document import Document
from app.infrastructure.database.session import get_db
from app.infrastructure.repositories.document_repository import (
    DocumentRepository,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=Document,
    status_code=201,
    summary="Upload a document and store its metadata.",
)
def upload_document(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload a document, process it, generate embeddings,
    and store chunks in PostgreSQL.
    """

    repository = DocumentRepository(db)

    storage = FileStorageService()

    use_case = UploadDocumentUseCase(
        repository=repository,
        storage=storage,
        db=db,
    )

    return use_case.execute(
        title=title,
        file=file,
    )