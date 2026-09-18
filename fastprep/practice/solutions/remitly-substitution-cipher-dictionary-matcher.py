# Approach: canonical isomorphism pattern (first-occurrence index encoding) + hash map bucketing of the dictionary.
from typing import List, Optional, Any


def _pattern(word: str) -> tuple:
    seen = {}
    out = []
    for ch in word:
        idx = seen.get(ch)
        if idx is None:
            idx = len(seen)
            seen[ch] = idx
        out.append(idx)
    return tuple(out)


def findCipherMatches(dictionary: List[str], queries: List[str]) -> List[List[str]]:
    buckets = {}
    for word in dictionary:
        buckets.setdefault(_pattern(word), []).append(word)
    return [list(buckets.get(_pattern(q), ())) for q in queries]
