from .db import get_connection
from .models import ContextResponse, SearchItem


def get_verse(reference: str, translation: str = "CUV") -> str | None:
    sql = """
    SELECT v.text
    FROM verses v
    JOIN translations t ON t.id = v.translation_id
    WHERE v.reference = %s AND t.code = %s
    LIMIT 1
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (reference, translation))
            row = cur.fetchone()
    return row["text"] if row else None


def compare_versions(reference: str) -> dict[str, str]:
    sql = """
    SELECT t.code, v.text
    FROM verses v
    JOIN translations t ON t.id = v.translation_id
    WHERE v.reference = %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (reference,))
            rows = cur.fetchall()
    return {row["code"]: row["text"] for row in rows}


def get_context(reference: str) -> ContextResponse | None:
    sql = """
    SELECT reference, book, author, theme, summary, nearby_refs
    FROM verse_contexts
    WHERE reference = %s
    LIMIT 1
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (reference,))
            row = cur.fetchone()

    if not row:
        return None

    nearby_refs = [x.strip() for x in (row["nearby_refs"] or "").split(",") if x.strip()]
    return ContextResponse(
        reference=row["reference"],
        book=row["book"],
        author=row["author"],
        theme=row["theme"],
        summary=row["summary"],
        nearby_refs=nearby_refs,
    )


def keyword_search(query: str, translation: str = "CUV", limit: int = 5) -> list[SearchItem]:
    q = query.strip()
    like_query = f"%{q}%"
    sql = """
    SELECT v.reference, v.text,
           CASE
             WHEN v.reference LIKE %s THEN 1.0
             WHEN v.text LIKE %s THEN 0.9
             ELSE 0.5
           END AS score
    FROM verses v
    JOIN translations t ON t.id = v.translation_id
    WHERE t.code = %s
      AND (v.reference LIKE %s OR v.text LIKE %s)
    ORDER BY score DESC, v.reference ASC
    LIMIT %s
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (like_query, like_query, translation, like_query, like_query, limit))
            rows = cur.fetchall()

    return [SearchItem(reference=row["reference"], text=row["text"], score=float(row["score"])) for row in rows]


def topic_refs(topic: str) -> list[str]:
    sql = """
    SELECT v.reference
    FROM topic_verses tv
    JOIN topics tp ON tp.id = tv.topic_id
    JOIN verses v ON v.id = tv.verse_id
    JOIN translations t ON t.id = v.translation_id
    WHERE tp.name = %s AND t.code = 'CUV'
    ORDER BY tv.sort_order ASC
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (topic,))
            rows = cur.fetchall()
    return [row["reference"] for row in rows]
