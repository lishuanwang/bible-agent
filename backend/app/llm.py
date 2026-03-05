import json
import os
from typing import Any
from urllib import request

from .models import SearchItem
from .prompts import SYSTEM_PROMPT, build_user_prompt


class LLMConfigError(RuntimeError):
    """Raised when LLM config is missing or invalid."""


def _chat_completion(messages: list[dict[str, str]]) -> str:
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")

    if not api_key:
        raise LLMConfigError("OPENAI_API_KEY is not set")

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.3,
    }

    req = request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    with request.urlopen(req, timeout=30) as resp:  # nosec B310
        response_payload: dict[str, Any] = json.loads(resp.read().decode("utf-8"))

    choices = response_payload.get("choices", [])
    if not choices:
        raise RuntimeError("LLM returned no choices")

    content = choices[0].get("message", {}).get("content", "")
    if not content:
        raise RuntimeError("LLM returned empty content")
    return content


def generate_answer(question: str, evidence: list[SearchItem], theology_profile: str) -> str:
    evidence_text = [f"{item.reference}: {item.text}" for item in evidence]
    user_prompt = (
        build_user_prompt(question, evidence_text)
        + f"\n神学立场配置：{theology_profile}\n"
        + "请严格按：结论、依据经文、背景解释、应用建议 输出。"
    )

    return _chat_completion(
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
    )


def devotional_plan(theme: str, refs: list[str], days: int) -> list[dict[str, str]]:
    refs = refs or ["Psalm 23:1"]
    return [
        {
            "day": str(day),
            "reference": refs[(day - 1) % len(refs)],
            "focus": f"围绕“{theme}”写下 1 条顺服行动。",
            "prayer": "主啊，求你借着你的话塑造我。",
        }
        for day in range(1, days + 1)
    ]


def sermon_outline(reference: str) -> dict[str, list[str] | str]:
    return {
        "title": f"从 {reference} 出发的讲章大纲",
        "outline": ["观察经文", "解释经文", "应用经文"],
        "group_questions": ["这段经文显明神什么属性？", "你本周如何实践？", "你需要谁与你同行？"],
    }


def prayer_guide(topic: str) -> dict[str, str]:
    return {
        "thanksgiving": f"主啊，感谢你在{topic}中仍掌权。",
        "confession": "求你赦免我常以自己为中心而不是先求你的旨意。",
        "supplication": f"求你赐下从你而来的智慧与平安面对{topic}。",
    }


def discipleship_plan(profile: str, weeks: int) -> list[dict[str, str]]:
    return [
        {
            "week": str(i),
            "goal": f"第{i}周：建立{profile}的祷告+读经+团契节奏",
            "practice": "每日15分钟读经祷告，每周一次小组分享",
        }
        for i in range(1, weeks + 1)
    ]
