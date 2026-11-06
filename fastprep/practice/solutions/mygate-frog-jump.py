# best[i] = min(best[i-1] + |h[i]-h[i-1]|, best[i-2] + |h[i]-h[i-2]|), kept in two rolling variables.
from typing import List, Optional, Any


def frogJump(heights: List[int]) -> int:
    n = len(heights)
    prev2, prev1 = 0, 0  # best for stones i-2 and i-1
    for i in range(1, n):
        cur = prev1 + abs(heights[i] - heights[i - 1])
        if i >= 2:
            cur = min(cur, prev2 + abs(heights[i] - heights[i - 2]))
        prev2, prev1 = prev1, cur
    return prev1
