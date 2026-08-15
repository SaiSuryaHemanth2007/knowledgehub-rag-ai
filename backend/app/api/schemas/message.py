from datetime import datetime

from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    """
    Request schema for creating a conversation message.
    """

    role: str = Field(
        ...,
        min_length=1,
        max_length=20,
    )

    content: str = Field(
        ...,
        min_length=1,
    )


class MessageResponse(BaseModel):
    """
    Response schema for a conversation message.
    """

    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }


class MessageListResponse(BaseModel):
    """
    Response schema for conversation message history.
    """

    messages: list[MessageResponse]