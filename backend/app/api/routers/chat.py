import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from app.application.services.conversation.conversation_service import (
    ConversationService,
)
from app.application.services.conversation.message_service import (
    MessageService,
)
from app.application.services.rag.rag_service import (
    RAGService,
)


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


# =========================================================
# Normal Chat
# =========================================================

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
    Standard non-streaming RAG endpoint.
    """

    conversation_service = ConversationService(db)
    message_service = MessageService(db)

    # -----------------------------------------------------
    # Resolve conversation
    # -----------------------------------------------------

    conversation_id = request.conversation_id

    if conversation_id is None:

        conversation = conversation_service.create(
            title=request.question[:255],
        )

        conversation_id = conversation.id

    else:

        conversation = conversation_service.get(
            conversation_id,
        )

        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found.",
            )

    # -----------------------------------------------------
    # Load previous history
    # -----------------------------------------------------

    history = message_service.get_history(
        conversation_id=conversation_id,
    )

    # -----------------------------------------------------
    # Set title from the first question
    #
    # If the frontend created the conversation as
    # "New Chat", rename it using the first question.
    # -----------------------------------------------------

    if (
        conversation.title == "New Chat"
        and not history
    ):
        conversation_service.update_title(
            conversation,
            request.question[:255],
        )

    # -----------------------------------------------------
    # Save user message
    # -----------------------------------------------------

    message_service.create(
        conversation_id=conversation_id,
        role="user",
        content=request.question,
    )

    # -----------------------------------------------------
    # Generate RAG answer
    # -----------------------------------------------------

    rag = RAGService(db)

    result = rag.ask(
        question=request.question,
        conversation_history=history,
    )

    # -----------------------------------------------------
    # Save assistant message
    # -----------------------------------------------------

    message_service.create(
        conversation_id=conversation_id,
        role="assistant",
        content=result["answer"],
    )

    # -----------------------------------------------------
    # Return response
    # -----------------------------------------------------

    return ChatResponse(
        answer=result["answer"],
        sources=result["sources"],
        conversation_id=conversation_id,
    )


# =========================================================
# Streaming Chat
# =========================================================

@router.post(
    "/stream",
    summary="Stream an answer from the uploaded documents.",
)
def stream_chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
):
    """
    Stream an answer using RAG while maintaining
    conversation history.
    """

    conversation_service = ConversationService(db)
    message_service = MessageService(db)

    # -----------------------------------------------------
    # Resolve conversation
    # -----------------------------------------------------

    conversation_id = request.conversation_id

    if conversation_id is None:

        conversation = conversation_service.create(
            title=request.question[:255],
        )

        conversation_id = conversation.id

    else:

        conversation = conversation_service.get(
            conversation_id,
        )

        if conversation is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found.",
            )

    # -----------------------------------------------------
    # Load previous history BEFORE saving current question
    # -----------------------------------------------------

    history = message_service.get_history(
        conversation_id=conversation_id,
    )

    # -----------------------------------------------------
    # Set title from the first question
    #
    # The frontend may create a conversation with the
    # default title "New Chat". When the first question
    # arrives, replace that title with the question.
    # -----------------------------------------------------

    if (
        conversation.title == "New Chat"
        and not history
    ):
        conversation_service.update_title(
            conversation,
            request.question[:255],
        )

    # -----------------------------------------------------
    # Save current user message
    # -----------------------------------------------------

    message_service.create(
        conversation_id=conversation_id,
        role="user",
        content=request.question,
    )

    # -----------------------------------------------------
    # Build RAG stream
    # -----------------------------------------------------

    rag = RAGService(db)

    token_stream, sources = rag.stream_ask(
        question=request.question,
        conversation_history=history,
    )

    def event_stream():
        """
        Convert the RAG token generator into
        Server-Sent Events.
        """

        accumulated_answer = ""

        try:

            # ---------------------------------------------
            # Stream tokens
            # ---------------------------------------------

            for token in token_stream:

                accumulated_answer += token

                yield (
                    "data: "
                    + json.dumps(
                        {
                            "type": "token",
                            "text": token,
                        }
                    )
                    + "\n\n"
                )

            # ---------------------------------------------
            # Save complete assistant answer
            # ---------------------------------------------

            if accumulated_answer:

                message_service.create(
                    conversation_id=conversation_id,
                    role="assistant",
                    content=accumulated_answer,
                )

            # ---------------------------------------------
            # Send completion event
            # ---------------------------------------------

            yield (
                "data: "
                + json.dumps(
                    {
                        "type": "done",
                        "conversation_id": conversation_id,
                        "sources": sources,
                    }
                )
                + "\n\n"
            )

        except Exception as exc:

            yield (
                "data: "
                + json.dumps(
                    {
                        "type": "error",
                        "message": str(exc),
                    }
                )
                + "\n\n"
            )

    # -----------------------------------------------------
    # Return streaming response
    # -----------------------------------------------------

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )