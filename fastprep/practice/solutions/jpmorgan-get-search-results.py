# Bucket words by sorted-letter signature, then look up each query's signature.
from typing import List, Optional, Any


def getSearchResults(words: List[str], queries: List[str]) -> List[List[str]]:
    buckets = {}
    for w in words:
        buckets.setdefault("".join(sorted(w)), []).append(w)
    for key in buckets:
        buckets[key].sort()
    return [list(buckets.get("".join(sorted(q)), [])) for q in queries]
