from fastapi import FastAPI, HTTPException

from .data import TOPIC_MAP
from .llm import devotional_plan, generate_answer, sermon_outline
from .models import (
    ChatRequest,
    ChatResponse,
    CompareVerseResponse,
    DevotionalPlanResponse,
    SearchItem,
    SermonOutlineResponse,
    TopicStudyResponse,
    VerseResponse,
    ContextResponse,
)
from .retrieval import compare_versions, get_context, get_verse, keyword_search
from .safety import detect_high_risk, escalation_message

app = FastAPI(title="Bible AI Agent API", version="0.2.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/verse", response_model=VerseResponse)
def verse(reference: str, translation: str = "CUV") -> VerseResponse:
    text = get_verse(reference, translation)
    if not text:
        raise HTTPException(status_code=404, detail="Verse not found")
    return VerseResponse(reference=reference, text=text, translation=translation)


@app.get("/compare", response_model=CompareVerseResponse)
def compare(reference: str) -> CompareVerseResponse:
    versions = compare_versions(reference)
    if not versions:
        raise HTTPException(status_code=404, detail="Verse not found in available translations")
    return CompareVerseResponse(reference=reference, versions=versions)


@app.get("/context", response_model=ContextResponse)
def context(reference: str) -> ContextResponse:
    ctx = get_context(reference)
    if not ctx:
        raise HTTPException(status_code=404, detail="Context not found")
    return ctx


@app.get("/search", response_model=list[SearchItem])
def search(q: str, translation: str = "CUV") -> list[SearchItem]:
    return keyword_search(q, translation=translation)


@app.get("/topic", response_model=TopicStudyResponse)
def topic_study(topic: str, translation: str = "CUV") -> TopicStudyResponse:
    refs = TOPIC_MAP.get(topic, [])
    verses = [SearchItem(reference=ref, text=get_verse(ref, translation) or "", score=0.9) for ref in refs]
    verses = [v for v in verses if v.text]
    return TopicStudyResponse(
        topic=topic,
        key_verses=verses,
        interpretation=f"主题“{topic}”建议结合上下文与整本圣经神学脉络来理解。",
        application_questions=[
            "这组经文揭示了神怎样的属性？",
            "你目前的处境与这些经文的连接点是什么？",
            "本周你可以采取什么具体顺服行动？",
        ],
    )


@app.get("/devotional", response_model=DevotionalPlanResponse)
def devotional(theme: str = "安慰", days: int = 7) -> DevotionalPlanResponse:
    refs = TOPIC_MAP.get(theme, ["Psalm 23:1"])
    plan = devotional_plan(theme, refs, days=max(1, min(days, 30)))
    return DevotionalPlanResponse(days=len(plan), theme=theme, plan=plan)


@app.get("/sermon", response_model=SermonOutlineResponse)
def sermon(reference: str, translation: str = "CUV") -> SermonOutlineResponse:
    text = get_verse(reference, translation)
    if not text:
        raise HTTPException(status_code=404, detail="Verse not found")
    generated = sermon_outline(reference, text)
    return SermonOutlineResponse(
        reference=reference,
        title=str(generated["title"]),
        outline=list(generated["outline"]),
        group_questions=list(generated["group_questions"]),
    )


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    safety_notice = escalation_message() if detect_high_risk(payload.question) else None
    evidence = keyword_search(payload.question, translation=payload.translation)
    answer = generate_answer(payload.question, evidence, payload.theology_profile)
    return ChatResponse(answer=answer, evidence=evidence, safety_notice=safety_notice)
