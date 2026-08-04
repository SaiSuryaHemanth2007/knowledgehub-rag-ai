from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.schemas.document import DocumentResponse
from app.application.services.file_storage import FileStorageService
from app.application.use_cases.upload_document import (
    UploadDocumentUseCase,
)
from app.infrastructure.repositories.document_repository import (
    DocumentRepository,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    title: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload a document and store its metadata.
    """

    repository = DocumentRepository(db)
    storage = FileStorageService()

    use_case = UploadDocumentUseCase(
        repository=repository,
        storage=storage,
    )

    return use_case.execute(
        title=title,
        file=file,
    )