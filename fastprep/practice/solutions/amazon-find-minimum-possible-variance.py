# Approach: variance telescopes over equal-value positions, so the answer is the
# minimum gap-1 between consecutive occurrences of the same height.
from typing import List, Optional, Any


def findMinimumVariance(height: List[int]) -> int:
    last = {}
    best = None
    for i, h in enumerate(height):
        if h in last:
            cand = i - last[h] - 1
            if best is None or cand < best:
                best = cand
                if best == 0:
                    # cannot do better than zero
                    best = 0
        last[h] = i
    return best if best is not None else -1
