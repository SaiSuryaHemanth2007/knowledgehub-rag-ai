from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
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


# =========================================================
# Upload Document
# =========================================================

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


# =========================================================
# Get All Documents
# =========================================================

@router.get(
    "",
    response_model=list[Document],
    summary="Get all uploaded documents.",
)
def get_documents(
    db: Session = Depends(get_db),
):
    """
    Retrieve all uploaded documents.
    """

    repository = DocumentRepository(db)

    return repository.get_all()


# =========================================================
# Get Document
# =========================================================

@router.get(
    "/{document_id}",
    response_model=Document,
    summary="Get a document by ID.",
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve an uploaded document by ID.
    """

    repository = DocumentRepository(db)

    document = repository.get_by_id(
        document_id,
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    return document


# =========================================================
# Delete Document
# =========================================================

@router.delete(
    "/{document_id}",
    status_code=204,
    summary="Delete an uploaded document.",
)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete an uploaded document, its stored file,
    and its database record.
    """

    repository = DocumentRepository(db)

    storage = FileStorageService()

    # -----------------------------------------------------
    # Find document
    # -----------------------------------------------------

    document = repository.get_by_id(
        document_id,
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    # -----------------------------------------------------
    # Delete physical file
    # -----------------------------------------------------

    storage.delete(
        document.stored_filename,
    )

    # -----------------------------------------------------
    # Delete database record
    # -----------------------------------------------------

    repository.delete(
        document_id,
    )

    return None