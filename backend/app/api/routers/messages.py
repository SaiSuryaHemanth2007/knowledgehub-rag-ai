from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.schemas.message import (
    MessageCreate,
    MessageListResponse,
    MessageResponse,
)
from app.application.services.conversation.conversation_service import (
    ConversationService,
)
from app.application.services.conversation.message_service import (
    MessageService,
)


router = APIRouter(
    prefix="/conversations/{conversation_id}/messages",
    tags=["Messages"],
)


# =========================================================
# Create Message
# =========================================================

@router.post(
    "",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a message in a conversation.",
)
def create_message(
    conversation_id: int,
    request: MessageCreate,
    db: Session = Depends(get_db),
):
    """
    Create a message inside an existing conversation.
    """

    # -----------------------------------------------------
    # Verify conversation exists
    # -----------------------------------------------------

    conversation_service = ConversationService(db)

    conversation = conversation_service.get(
        conversation_id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )

    # -----------------------------------------------------
    # Create message
    # -----------------------------------------------------

    message_service = MessageService(db)

    message = message_service.create(
        conversation_id=conversation_id,
        role=request.role,
        content=request.content,
    )

    return message


# =========================================================
# Get Conversation Messages
# =========================================================

@router.get(
    "",
    response_model=MessageListResponse,
    summary="Get messages from a conversation.",
)
def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve all messages belonging to a conversation.
    """

    # -----------------------------------------------------
    # Verify conversation exists
    # -----------------------------------------------------

    conversation_service = ConversationService(db)

    conversation = conversation_service.get(
        conversation_id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )

    # -----------------------------------------------------
    # Retrieve messages
    # -----------------------------------------------------

    message_service = MessageService(db)

    messages = message_service.get_history(
        conversation_id,
    )

    return {
        "messages": messages,
    }