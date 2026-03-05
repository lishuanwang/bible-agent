from .models import SearchItem


def generate_answer(question: str, evidence: list[SearchItem], theology_profile: str) -> str:
    if not evidence:
        return (
            "结论：我暂时没有检索到足够证据。\n"
            "依据经文：暂无。\n"
            "背景解释：请提供更具体的圣经主题或经文范围。\n"
            "应用建议：可先从福音书、诗篇、罗马书开始。"
        )

    evidence_lines = "\n".join([f"- {item.reference}：{item.text}" for item in evidence])
    return (
        "结论：以下为基于经文证据的回应。\n"
        f"依据经文：\n{evidence_lines}\n"
        "背景解释：建议结合上下文、作者与原受众进行解释。\n"
        f"神学立场提示：当前配置为 {theology_profile}。\n"
        "应用建议：祷告、默想、与教会群体讨论并实践。"
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
