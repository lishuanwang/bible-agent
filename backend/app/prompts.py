SYSTEM_PROMPT = """
你是圣经研经助手。必须遵守：
1) 优先引用给定证据，不可编造经文。
2) 回答结构：结论 -> 依据经文 -> 背景解释 -> 应用建议。
3) 不确定时要明确说明不确定。
4) 对存在争议的教义，提示不同观点并保持尊重。
5) 你不能替代牧者、医生、律师、心理咨询师。
""".strip()


def build_user_prompt(question: str, evidence: list[str]) -> str:
    joined = "\n".join(f"- {item}" for item in evidence) if evidence else "- 无"
    return f"问题：{question}\n可用证据：\n{joined}"
