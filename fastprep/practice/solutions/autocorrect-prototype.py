# Hash dictionary words by their sorted-letter signature, then look up each query.
from typing import List, Optional, Any


def autocorrectPrototype(n: int, words: List[str], queries: List[str]) -> List[List[str]]:
    buckets = {}
    for w in words:
        buckets.setdefault("".join(sorted(w)), []).append(w)
    for key in buckets:
        buckets[key].sort()

    result = []
    for q in queries[:n] if n is not None else queries:
        result.append(list(buckets.get("".join(sorted(q)), [])))
    return result
