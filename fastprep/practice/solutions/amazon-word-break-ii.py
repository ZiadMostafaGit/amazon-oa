# Memoized DFS over suffixes, collecting all segmentations; results sorted lexicographically.
from functools import lru_cache
from typing import List


def solve(s: str, wordDict: List[str]) -> List[str]:
    words = set(wordDict)
    if not words:
        return []
    maxlen = max(len(w) for w in words)
    n = len(s)

    @lru_cache(maxsize=None)
    def build(i: int) -> List[str]:
        if i == n:
            return [""]
        res = []
        for j in range(i + 1, min(n, i + maxlen) + 1):
            head = s[i:j]
            if head in words:
                for tail in build(j):
                    res.append(head if not tail else head + " " + tail)
        return res

    out = build(0)
    build.cache_clear()
    return sorted(out)
