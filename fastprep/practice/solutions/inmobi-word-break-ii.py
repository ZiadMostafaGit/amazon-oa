# Memoized DFS over suffixes collecting all segmentations, then sorted lexicographically.
from typing import List, Optional, Any


def wordBreak(s: str, wordDict: List[str]) -> List[str]:
    words = set(wordDict)
    if not words:
        return []
    maxlen = max(len(w) for w in words)
    n = len(s)
    memo = {}

    def dfs(i: int) -> List[str]:
        if i == n:
            return [""]
        if i in memo:
            return memo[i]
        res = []
        limit = min(n, i + maxlen)
        for j in range(i + 1, limit + 1):
            w = s[i:j]
            if w in words:
                for rest in dfs(j):
                    res.append(w if rest == "" else w + " " + rest)
        memo[i] = res
        return res

    out = sorted(set(dfs(0)))
    return out
