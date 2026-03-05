HIGH_RISK_KEYWORDS = ["自杀", "自残", "伤害自己", "家暴", "暴力"]

OFF_TOPIC_KEYWORDS = [
    "炒股",
    "彩票",
    "游戏外挂",
    "加密货币短线",
    "八卦",
    "星座",
]


def detect_high_risk(text: str) -> bool:
    normalized = text.strip().lower()
    return any(keyword in normalized for keyword in HIGH_RISK_KEYWORDS)


def detect_off_topic(text: str) -> bool:
    normalized = text.strip().lower()
    return any(keyword in normalized for keyword in OFF_TOPIC_KEYWORDS)


def escalation_message() -> str:
    return (
        "你提到的内容可能涉及高风险情境。"
        "请尽快联系当地紧急热线、可信任的牧者/家人，"
        "并考虑寻求专业心理或医疗支持。"
        "我可以继续提供安慰经文，但无法替代专业援助。"
    )


def scope_message() -> str:
    return "本助手专注圣经与基督教内容。我可以把你的问题转成圣经视角来一起讨论。"
