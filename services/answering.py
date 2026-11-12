import re
import unicodedata

STOPWORDS = {
    "les", "des", "une", "que", "qui", "quoi", "est", "sont", "dans", "pour",
    "par", "sur", "avec", "quel", "quelle", "quels", "quelles", "comment",
    "pourquoi", "ces", "cet", "cette", "aux", "pas", "plus", "ses", "son",
}


def normalize(text):
    text = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in text if unicodedata.category(c) != "Mn")


def keywords(text):
    words = re.findall(r"[a-z0-9]+", normalize(text))
    return {w for w in words if len(w) > 2 and w not in STOPWORDS}


def split_passages(content):
    parts = re.split(r"(?<=[.!?])\s+|\n+", content)
    return [p.strip() for p in parts if p.strip()]


def answer(question, courses, max_results=3):
    """Retourne les passages de cours les plus proches de la question."""
    q = keywords(question)
    if not q:
        return []
    scored = []
    for course in courses:
        for passage in split_passages(course["content"]):
            score = len(q & keywords(passage))
            if score > 0:
                scored.append((score, course["title"], passage))
    scored.sort(key=lambda item: -item[0])
    return scored[:max_results]