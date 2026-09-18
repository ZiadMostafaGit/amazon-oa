# Exact-match set lookup first, then a lowercase-key hash map for the case-insensitive correction.
from typing import List, Optional, Any


def autocorrect(dictionary: List[str], word: str) -> str:
    exact = set(dictionary)
    if word in exact:
        return word
    folded = {}
    for entry in dictionary:
        folded.setdefault(entry.lower(), entry)
    return folded.get(word.lower(), word)
