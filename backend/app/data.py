"""In-memory seed data for full-feature MVP.

Production should replace this with PostgreSQL + pgvector + proper licensed texts.
"""

VERSE_DATA = {
    "CUV": {
        "John 3:16": "神爱世人，甚至将他的独生子赐给他们，叫一切信他的，不至灭亡，反得永生。",
        "John 3:17": "因为神差他的儿子降世，不是要定世人的罪，乃是要叫世人因他得救。",
        "Romans 8:28": "我们晓得万事都互相效力，叫爱神的人得益处，就是按他旨意被召的人。",
        "Psalm 23:1": "耶和华是我的牧者，我必不至缺乏。",
        "Philippians 4:6": "应当一无挂虑，只要凡事借着祷告、祈求，和感谢，将你们所要的告诉神。",
    },
    "NIV": {
        "John 3:16": "For God so loved the world that he gave his one and only Son, that whoever believes in him shall not perish but have eternal life.",
        "John 3:17": "For God did not send his Son into the world to condemn the world, but to save the world through him.",
        "Romans 8:28": "And we know that in all things God works for the good of those who love him, who have been called according to his purpose.",
        "Psalm 23:1": "The Lord is my shepherd, I lack nothing.",
        "Philippians 4:6": "Do not be anxious about anything, but in every situation, by prayer and petition, with thanksgiving, present your requests to God.",
    },
}

VERSE_CONTEXT = {
    "John 3:16": {
        "book": "John",
        "author": "使徒约翰",
        "theme": "救恩与神的爱",
        "summary": "耶稣与尼哥底母对话，强调重生与信子的救恩。",
        "nearby_refs": ["John 3:14", "John 3:17", "John 3:18"],
    },
    "Romans 8:28": {
        "book": "Romans",
        "author": "使徒保罗",
        "theme": "苦难中的盼望与神的主权",
        "summary": "罗马书第八章讨论圣灵里的生活、苦难和荣耀盼望。",
        "nearby_refs": ["Romans 8:26", "Romans 8:29", "Romans 8:31"],
    },
}

TOPIC_MAP = {
    "安慰": ["Psalm 23:1", "Romans 8:28"],
    "焦虑": ["Philippians 4:6", "Psalm 23:1"],
    "救恩": ["John 3:16", "John 3:17"],
    "祷告": ["Philippians 4:6", "Psalm 23:1"],
}
