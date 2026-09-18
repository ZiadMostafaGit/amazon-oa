# Approach: suffix DP where best[i] = gameVal[i] + best[i+k], take the maximum start.
from typing import List, Optional, Any


def maxGameScore(gameVal: List[int], k: int) -> int:
    n = len(gameVal)
    best = [0] * n
    ans = None
    for i in range(n - 1, -1, -1):
        nxt = best[i + k] if i + k < n else 0
        best[i] = gameVal[i] + nxt
        if ans is None or best[i] > ans:
            ans = best[i]
    return ans if ans is not None else 0
