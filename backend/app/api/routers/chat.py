from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
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


# -------------------------------------------------------
# Normal Chat Endpoint
# -------------------------------------------------------

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
    Standard (non-streaming) RAG endpoint.
    """

    rag = RAGService(db)

    result = rag.ask(
        question=request.question,
    )

    print("\n========== RAG RESULT ==========")
    print(result)
    print("================================\n")

    return ChatResponse(**result)


# -------------------------------------------------------
# Streaming Chat Endpoint
# -------------------------------------------------------

@router.post(
    "/stream",
    summary="Stream an answer from the uploaded documents.",
)
def stream_chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Stream an answer token-by-token using
    Retrieval-Augmented Generation.
    """

    rag = RAGService(db)

    return StreamingResponse(
        rag.stream_ask(
            question=request.question,
        ),
        media_type="text/plain",
    )