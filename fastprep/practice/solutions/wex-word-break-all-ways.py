# Memoized DFS over suffixes collecting all segmentations, then sorted lexicographically.
from typing import List, Optional, Any
from functools import lru_cache


def wordBreak(s: str, wordDict: List[str]) -> List[str]:
    words = set(wordDict)
    maxlen = max((len(w) for w in words), default=0)
    n = len(s)

    @lru_cache(maxsize=None)
    def solve(i: int) -> tuple:
        if i == n:
            return ("",)
        out = []
        for j in range(i + 1, min(n, i + maxlen) + 1):
            w = s[i:j]
            if w in words:
                for rest in solve(j):
                    out.append(w if rest == "" else w + " " + rest)
        return tuple(out)

    res = list(solve(0))
    solve.cache_clear()
    res.sort()
    return res
