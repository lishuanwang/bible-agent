from fastapi import FastAPI, HTTPException

from .llm import generate_answer
from .models import ChatRequest, ChatResponse, SearchItem, VerseResponse
from .retrieval import get_verse, keyword_search
from .safety import detect_high_risk, escalation_message

app = FastAPI(title="Bible AI Agent API", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/verse", response_model=VerseResponse)
def verse(reference: str, translation: str = "CUV") -> VerseResponse:
    text = get_verse(reference)
    if not text:
        raise HTTPException(status_code=404, detail="Verse not found")
    return VerseResponse(reference=reference, text=text, translation=translation)


@app.get("/search", response_model=list[SearchItem])
def search(q: str) -> list[SearchItem]:
    return keyword_search(q)


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    safety_notice = escalation_message() if detect_high_risk(payload.question) else None
    evidence = keyword_search(payload.question)
    answer = generate_answer(payload.question, evidence)
    return ChatResponse(answer=answer, evidence=evidence, safety_notice=safety_notice)
