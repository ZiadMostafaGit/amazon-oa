# DP over values: best[x] = longest chain ending at value x, extended from value x ^ k.
from typing import List, Optional, Any


def maxSubsequenceLength(n: int, arr: List[int], k: int) -> int:
    best = {}
    ans = 0
    for x in arr:
        cand = best.get(x ^ k, 0) + 1
        if cand > best.get(x, 0):
            best[x] = cand
        if best[x] > ans:
            ans = best[x]
    return ans if ans >= 2 else 0
