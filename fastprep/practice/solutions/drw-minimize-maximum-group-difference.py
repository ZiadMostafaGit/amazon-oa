# Sort: some optimal answer uses three contiguous runs of the sorted array.
# Binary search the allowed difference D; greedily open a group at the smallest
# uncovered value and extend it to everything <= start + D. D works if <= 3 groups suffice.
from bisect import bisect_right
from typing import List, Optional, Any


def solution(A: List[int]) -> int:
    a = sorted(A)
    n = len(a)

    def groups(D: int) -> int:
        i, g = 0, 0
        while i < n:
            g += 1
            if g > 3:
                return g
            i = bisect_right(a, a[i] + D)
        return g

    lo, hi = 0, a[-1] - a[0]
    while lo < hi:
        mid = (lo + hi) // 2
        if groups(mid) <= 3:
            hi = mid
        else:
            lo = mid + 1
    return lo
