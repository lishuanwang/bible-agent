from .data import VERSES
from .models import SearchItem


def get_verse(reference: str) -> str | None:
    return VERSES.get(reference)


def keyword_search(query: str, limit: int = 5) -> list[SearchItem]:
    q = query.strip()
    results: list[SearchItem] = []
    for ref, text in VERSES.items():
        if q in text or q.lower() in ref.lower():
            results.append(SearchItem(reference=ref, text=text, score=1.0))
    return results[:limit]
