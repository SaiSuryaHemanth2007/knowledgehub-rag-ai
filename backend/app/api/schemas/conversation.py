from datetime import datetime

from pydantic import BaseModel, Field


# =========================================================
# Create Conversation
# =========================================================


class ConversationCreate(BaseModel):
    """
    Request schema for creating a conversation.
    """

    title: str = Field(
        default="New Chat",
        min_length=1,
        max_length=255,
    )


# =========================================================
# Conversation Response
# =========================================================


class ConversationResponse(BaseModel):
    """
    Response schema for a conversation.
    """

    id: int
    title: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True,
    }


# =========================================================
# Conversation List Response
# =========================================================


class ConversationListResponse(BaseModel):
    """
    Response schema for a list of conversations.
    """

    conversations: list[ConversationResponse]