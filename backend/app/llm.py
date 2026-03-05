from .models import SearchItem


def generate_answer(question: str, evidence: list[SearchItem], theology_profile: str) -> str:
    if not evidence:
        return (
            "结论：我暂时没有检索到足够证据。\n"
            "依据经文：暂无。\n"
            "背景解释：建议缩小问题范围，提供具体经文或主题关键词。\n"
            "应用建议：可先从诗篇、福音书或腓立比书相关章节开始查考。"
        )

    evidence_lines = "\n".join([f"- {item.reference}：{item.text}" for item in evidence])
    return (
        "结论：以下为基于已检索经文的回应。\n"
        f"依据经文：\n{evidence_lines}\n"
        "背景解释：请结合上下文、作者与受众来理解经文原意。\n"
        f"神学立场提示：当前配置为 {theology_profile}，争议议题请对照教会教导。\n"
        "应用建议：可将经文用于祷告、默想、记录行动步骤，并与属灵同伴讨论。"
    )


def devotional_plan(theme: str, refs: list[str], days: int) -> list[dict[str, str]]:
    if not refs:
        refs = ["Psalm 23:1"]
    plan: list[dict[str, str]] = []
    for day in range(1, days + 1):
        ref = refs[(day - 1) % len(refs)]
        plan.append(
            {
                "day": str(day),
                "reference": ref,
                "focus": f"围绕“{theme}”默想经文并写下一个顺服行动。",
                "prayer": "主啊，求你借着你的话引导我今天的心与脚步。",
            }
        )
    return plan


def sermon_outline(reference: str, verse_text: str) -> dict[str, list[str] | str]:
    return {
        "title": f"从 {reference} 看神的话语如何进入生活",
        "outline": [
            "一、观察：经文说了什么（关键词、重复、上下文）",
            "二、解释：经文对原始读者的意义是什么",
            "三、应用：今天如何活出这段经文",
        ],
        "group_questions": [
            f"{reference} 对你当前处境最触动的一句话是什么？",
            "你认为这段经文最需要被纠正的误解是什么？",
            "本周你愿意实践的一个具体行动是什么？",
        ],
        "verse_text": verse_text,
    }
