from fastapi import FastAPI, HTTPException

from .data import TOPIC_MAP
from .llm import (
    LLMConfigError,
    devotional_plan,
    discipleship_plan,
    generate_answer,
    prayer_guide,
    sermon_outline,
)
from .models import (
    ChatRequest,
    ChatResponse,
    CompareVerseResponse,
    ContextResponse,
    DevotionalPlanResponse,
    DiscipleshipPlanResponse,
    GroupSessionResponse,
    LifeScenarioResponse,
    PrayerGuideResponse,
    SearchItem,
    SermonOutlineResponse,
    TopicStudyResponse,
    VerseResponse,
)
from .retrieval import compare_versions, get_context, get_verse, keyword_search
from .safety import detect_high_risk, detect_off_topic, escalation_message, scope_message

app = FastAPI(title="Bible AI Agent API", version="0.3.0")


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
        interpretation=f"主题“{topic}”建议放在整本圣经启示脉络中理解。",
        application_questions=["神的心意是什么？", "我需要悔改什么？", "本周如何顺服？"],
    )


@app.get("/devotional", response_model=DevotionalPlanResponse)
def devotional(theme: str = "安慰", days: int = 7) -> DevotionalPlanResponse:
    refs = TOPIC_MAP.get(theme, ["Psalm 23:1"])
    bounded_days = max(1, min(days, 30))
    return DevotionalPlanResponse(days=bounded_days, theme=theme, plan=devotional_plan(theme, refs, bounded_days))


@app.get("/sermon", response_model=SermonOutlineResponse)
def sermon(reference: str) -> SermonOutlineResponse:
    text = get_verse(reference, "CUV")
    if not text:
        raise HTTPException(status_code=404, detail="Verse not found")
    generated = sermon_outline(reference)
    return SermonOutlineResponse(
        reference=reference,
        title=str(generated["title"]),
        outline=list(generated["outline"]),
        group_questions=list(generated["group_questions"]),
    )


@app.get("/prayer", response_model=PrayerGuideResponse)
def prayer(topic: str = "焦虑", translation: str = "CUV") -> PrayerGuideResponse:
    refs = TOPIC_MAP.get(topic, ["Philippians 4:6"])
    scripture = [SearchItem(reference=r, text=get_verse(r, translation) or "", score=0.9) for r in refs]
    scripture = [item for item in scripture if item.text]
    blocks = prayer_guide(topic)
    return PrayerGuideResponse(topic=topic, scripture=scripture, **blocks)


@app.get("/discipleship", response_model=DiscipleshipPlanResponse)
def discipleship(profile: str = "初信者", weeks: int = 8) -> DiscipleshipPlanResponse:
    bounded_weeks = max(1, min(weeks, 24))
    return DiscipleshipPlanResponse(profile=profile, weeks=bounded_weeks, milestones=discipleship_plan(profile, bounded_weeks))


@app.get("/life-scenario", response_model=LifeScenarioResponse)
def life_scenario(scenario: str, translation: str = "CUV") -> LifeScenarioResponse:
    refs = TOPIC_MAP.get(scenario, TOPIC_MAP.get("智慧", []))
    passages = [SearchItem(reference=r, text=get_verse(r, translation) or "", score=0.8) for r in refs]
    passages = [item for item in passages if item.text]
    return LifeScenarioResponse(
        scenario=scenario,
        biblical_principles=["先求神的国", "在真理里彼此相爱", "以祷告寻求智慧"],
        suggested_passages=passages,
        action_steps=["列出当前挑战", "对照经文写下顺服行动", "向牧者或小组寻求同行"],
    )


@app.get("/group-session", response_model=GroupSessionResponse)
def group_session(theme: str = "安慰", translation: str = "CUV") -> GroupSessionResponse:
    refs = TOPIC_MAP.get(theme, ["Psalm 23:1"])
    passages = [SearchItem(reference=r, text=get_verse(r, translation) or "", score=0.8) for r in refs]
    passages = [item for item in passages if item.text]
    return GroupSessionResponse(
        theme=theme,
        icebreaker="请每位成员分享最近一周最感恩的一件事。",
        passages=passages,
        flow=["破冰与祷告", "观察经文", "解释与讨论", "应用与代祷"],
    )


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    safety_notice = escalation_message() if detect_high_risk(payload.question) else None
    scope_notice = scope_message() if detect_off_topic(payload.question) else None
    evidence = keyword_search(payload.question, translation=payload.translation)
    try:
        answer = generate_answer(payload.question, evidence, payload.theology_profile)
    except LLMConfigError as exc:
        raise HTTPException(status_code=503, detail=f"LLM config error: {exc}") from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM request failed: {exc}") from exc
    return ChatResponse(answer=answer, evidence=evidence, safety_notice=safety_notice, scope_notice=scope_notice)
