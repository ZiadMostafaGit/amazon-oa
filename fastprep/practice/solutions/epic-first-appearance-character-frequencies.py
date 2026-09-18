# Single pass counting with an insertion-ordered dict keyed by lowercase letter.
from typing import List, Optional, Any


def orderedCharacterFrequencies(text: str) -> List[str]:
    counts = {}
    for ch in text:
        if ch.isspace():
            continue
        if not ch.isalpha():
            continue
        c = ch.lower()
        counts[c] = counts.get(c, 0) + 1
    return ["%s:%d" % (c, n) for c, n in counts.items()]
