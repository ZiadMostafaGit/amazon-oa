# Approach: binary search on the saw height, using the monotone decreasing total-wood function.
from typing import List


def solve(heights: List[int], requiredWood: int) -> int:
    def wood(h: int) -> int:
        return sum(x - h for x in heights if x > h)

    if wood(0) < requiredWood:
        return -1
    lo, hi = 0, max(heights) if heights else 0
    best = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if wood(mid) >= requiredWood:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best
