# Binary search on the eating rate (Koko-eating-bananas pattern).
from typing import List, Optional, Any


def minDonutsPerMinute(donutBoxes: List[int], numMinutes: int) -> int:
    lo, hi = 1, max(donutBoxes)
    while lo < hi:
        mid = (lo + hi) // 2
        minutes = sum((b + mid - 1) // mid for b in donutBoxes)
        if minutes <= numMinutes:
            hi = mid
        else:
            lo = mid + 1
    return lo
