# Hash-count both windows, then sort by (-count, url) and take the first k of each.
from typing import List, Optional, Any
from collections import Counter


def _top(counter: Counter, k: int) -> List[str]:
    items = sorted(counter.items(), key=lambda kv: (-kv[1], kv[0]))
    return [u for u, _ in items[:k]]


def topKUrls(urls: List[str], timestamps: List[int], queryTime: int, k: int) -> List[List[str]]:
    overall = Counter()
    recent = Counter()
    lo = queryTime - 86400
    for u, t in zip(urls, timestamps):
        overall[u] += 1
        if lo <= t <= queryTime:
            recent[u] += 1
    return [_top(overall, k), _top(recent, k)]
