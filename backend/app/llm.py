from .models import SearchItem


def generate_answer(question: str, evidence: list[SearchItem]) -> str:
    if not evidence:
        return (
            "我暂时没有检索到足够经文证据。"
            "建议你提供更具体的经文范围（例如 John 3:16）或关键词。"
        )

    evidence_lines = "\n".join([f"{item.reference}：{item.text}" for item in evidence])
    return (
        "结论：以下是基于已检索经文的简要回应。\n"
        f"依据经文：\n{evidence_lines}\n"
        "背景解释：请结合章节上下文进一步查考。\n"
        "应用建议：可将经文用于祷告、默想与小组讨论。"
    )
