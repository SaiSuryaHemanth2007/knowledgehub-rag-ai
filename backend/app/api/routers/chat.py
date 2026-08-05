from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.application.services.rag.rag_service import (
    RAGService,
)

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
    summary="Ask a question about the uploaded documents.",
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Ask a question about the uploaded documents.
    """

    rag = RAGService(db)

    result = rag.ask(
        question=request.question,
    )

    # Debug output
    print("\n========== RAG RESULT ==========")
    print(result)
    print("================================\n")

    return ChatResponse(**result)