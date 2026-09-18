# Linear scan keeping the minimum value strictly inside the open interval.
from typing import List, Optional, Any


def findLowestInRange(numbers: List[int], nRange: List[int]) -> int:
    lo, hi = nRange[0], nRange[1]
    best = None
    for v in numbers:
        if lo < v < hi and (best is None or v < best):
            best = v
    return 0 if best is None else best
