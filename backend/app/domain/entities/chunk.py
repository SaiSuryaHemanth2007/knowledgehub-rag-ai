from dataclasses import dataclass


@dataclass
class Chunk:
    """
    Represents a chunk of extracted document text.
    """

    document_id: int

    chunk_index: int

    content: str