HIGH_RISK_KEYWORDS = [
    "自杀",
    "自残",
    "伤害自己",
    "家暴",
    "暴力",
]


def detect_high_risk(text: str) -> bool:
    normalized = text.strip().lower()
    return any(keyword in normalized for keyword in HIGH_RISK_KEYWORDS)


def escalation_message() -> str:
    return (
        "你提到的内容可能涉及高风险情境。"
        "请尽快联系当地紧急热线、可信任的牧者/家人，"
        "并考虑寻求专业心理或医疗支持。"
        "我可以继续提供安慰经文，但无法替代专业援助。"
    )
