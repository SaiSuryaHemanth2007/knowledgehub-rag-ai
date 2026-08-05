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