from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DocumentCreate(BaseModel):
    """
    Request schema for creating a document.
    """

    title: str
    original_filename: str
    stored_filename: str
    file_type: str
    file_size: int


class DocumentResponse(BaseModel):
    """
    Response schema.
    """

    id: int
    title: str
    original_filename: str
    stored_filename: str
    file_type: str
    file_size: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)