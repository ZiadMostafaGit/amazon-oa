# Binary search the smallest step x with sum(ceil(score / x)) <= maxAdjustments.
from typing import List, Optional, Any


def getMinAdjustments(videoScores: List[int], maxAdjustments: int) -> int:
    lo, hi = 1, max(videoScores)
    while lo < hi:
        mid = (lo + hi) // 2
        ops = 0
        for s in videoScores:
            ops += (s + mid - 1) // mid
            if ops > maxAdjustments:
                break
        if ops <= maxAdjustments:
            hi = mid
        else:
            lo = mid + 1
    return lo
