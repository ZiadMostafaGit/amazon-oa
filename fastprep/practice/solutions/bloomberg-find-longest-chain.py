# Longest string chain: DP by increasing word length over single-letter-deletion predecessors.
from typing import List, Optional, Any


def longestChain(words: List[str]) -> int:
    present = set(words)
    best = {}
    ans = 0
    for w in sorted(present, key=len):
        cur = 1
        for i in range(len(w)):
            prev = w[:i] + w[i + 1:]
            if prev in best:
                cand = best[prev] + 1
                if cand > cur:
                    cur = cand
        best[w] = cur
        if cur > ans:
            ans = cur
    return ans
