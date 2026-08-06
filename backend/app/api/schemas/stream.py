from pydantic import BaseModel


class StreamToken(BaseModel):
    text: str


class StreamDone(BaseModel):
    sources: list