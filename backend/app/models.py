from pydantic import BaseModel, Field


class VerseResponse(BaseModel):
    reference: str
    text: str
    translation: str = "CUV"


class SearchItem(BaseModel):
    reference: str
    text: str
    score: float = Field(default=1.0)


class ChatRequest(BaseModel):
    question: str
    translation: str = "CUV"
    theology_profile: str = "evangelical"


class ChatResponse(BaseModel):
    answer: str
    evidence: list[SearchItem]
    safety_notice: str | None = None
