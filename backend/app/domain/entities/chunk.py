from dataclasses import dataclass


@dataclass
class Chunk:
    """
    Pure domain entity representing a chunk of text.
    """

    document_id: int
    chunk_index: int
    content: str