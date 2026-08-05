from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Document:
    """
    Pure domain entity representing a document.
    """

    id: Optional[int] = None

    title: str = ""

    original_filename: str = ""

    stored_filename: str = ""

    file_type: str = ""

    file_size: int = 0

    status: str = "uploaded"

    created_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None