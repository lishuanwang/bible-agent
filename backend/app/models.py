from pydantic import BaseModel, Field


class VerseResponse(BaseModel):
    reference: str
    text: str
    translation: str = "CUV"


class SearchItem(BaseModel):
    reference: str
    text: str
    score: float = Field(default=1.0)


class CompareVerseResponse(BaseModel):
    reference: str
    versions: dict[str, str]


class ContextResponse(BaseModel):
    reference: str
    book: str
    author: str
    theme: str
    summary: str
    nearby_refs: list[str]


class TopicStudyResponse(BaseModel):
    topic: str
    key_verses: list[SearchItem]
    interpretation: str
    application_questions: list[str]


class DevotionalPlanResponse(BaseModel):
    days: int
    theme: str
    plan: list[dict[str, str]]


class SermonOutlineResponse(BaseModel):
    reference: str
    title: str
    outline: list[str]
    group_questions: list[str]


class PrayerGuideResponse(BaseModel):
    topic: str
    scripture: list[SearchItem]
    thanksgiving: str
    confession: str
    supplication: str


class DiscipleshipPlanResponse(BaseModel):
    profile: str
    weeks: int
    milestones: list[dict[str, str]]


class LifeScenarioResponse(BaseModel):
    scenario: str
    biblical_principles: list[str]
    suggested_passages: list[SearchItem]
    action_steps: list[str]


class GroupSessionResponse(BaseModel):
    theme: str
    icebreaker: str
    passages: list[SearchItem]
    flow: list[str]


class ChatRequest(BaseModel):
    question: str
    translation: str = "CUV"
    theology_profile: str = "evangelical"


class ChatResponse(BaseModel):
    answer: str
    evidence: list[SearchItem]
    safety_notice: str | None = None
    scope_notice: str | None = None
