from .data import TOPIC_MAP, VERSE_CONTEXT, VERSE_DATA
from .models import ContextResponse, SearchItem


def get_verse(reference: str, translation: str = "CUV") -> str | None:
    return VERSE_DATA.get(translation, {}).get(reference)


def compare_versions(reference: str) -> dict[str, str]:
    return {
        translation: verses[reference]
        for translation, verses in VERSE_DATA.items()
        if reference in verses
    }


def get_context(reference: str) -> ContextResponse | None:
    ctx = VERSE_CONTEXT.get(reference)
    if not ctx:
        return None
    return ContextResponse(reference=reference, **ctx)


def keyword_search(query: str, translation: str = "CUV", limit: int = 5) -> list[SearchItem]:
    q = query.strip().lower()
    results: list[SearchItem] = []
    verses = VERSE_DATA.get(translation, {})

    for ref, text in verses.items():
        if not q:
            continue
        if q in text.lower() or q in ref.lower():
            results.append(SearchItem(reference=ref, text=text, score=1.0))

    if not results:
        for topic, refs in TOPIC_MAP.items():
            if topic in query:
                for ref in refs:
                    verse = verses.get(ref)
                    if verse:
                        results.append(SearchItem(reference=ref, text=verse, score=0.8))

    return results[:limit]
