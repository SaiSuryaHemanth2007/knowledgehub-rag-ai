from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.api.schemas.conversation import (
    ConversationCreate,
    ConversationListResponse,
    ConversationResponse,
)
from app.application.services.conversation.conversation_service import (
    ConversationService,
)


router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


# =========================================================
# Create Conversation
# =========================================================

@router.post(
    "",
    response_model=ConversationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new conversation.",
)
def create_conversation(
    request: ConversationCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new chat conversation.
    """

    service = ConversationService(db)

    conversation = service.create(
        title=request.title,
    )

    return conversation


# =========================================================
# Get All Conversations
# =========================================================

@router.get(
    "",
    response_model=ConversationListResponse,
    summary="Get all conversations.",
)
def get_conversations(
    db: Session = Depends(get_db),
):
    """
    Retrieve all conversations ordered by
    most recently updated.
    """

    service = ConversationService(db)

    conversations = service.list_all()

    return {
        "conversations": conversations,
    }


# =========================================================
# Get Conversation
# =========================================================

@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
    summary="Get a conversation by ID.",
)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    """
    Retrieve a conversation by ID.
    """

    service = ConversationService(db)

    conversation = service.get(
        conversation_id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )

    return conversation


# =========================================================
# Delete Conversation
# =========================================================

@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a conversation.",
)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a conversation and its messages.
    """

    service = ConversationService(db)

    deleted = service.delete(
        conversation_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found.",
        )

    return None