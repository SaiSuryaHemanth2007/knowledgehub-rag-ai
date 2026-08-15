from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """
    Chat request.
    """

    question: str = Field(
        ...,
        min_length=1,
        description="User question",
    )

    conversation_id: int | None = Field(
        default=None,
        description="Existing conversation ID.",
    )


class SourceResponse(BaseModel):
    """
    Source metadata.
    """

    document_id: int
    document_title: str
    original_filename: str
    chunk_index: int
    score: float
    preview: str


class ChatResponse(BaseModel):
    """
    Chat response.
    """

    answer: str
    sources: list[SourceResponse]

    conversation_id: int | None = None