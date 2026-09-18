# Binary search on the answer (minimum gap), greedy feasibility check.
from typing import List, Optional, Any


def solve(stalls: List[int], cows: int) -> int:
    pos = sorted(stalls)
    n = len(pos)
    if cows <= 1:
        return 0

    def can(gap: int) -> bool:
        placed = 1
        last = pos[0]
        for x in pos[1:]:
            if x - last >= gap:
                placed += 1
                last = x
                if placed >= cows:
                    return True
        return placed >= cows

    lo, hi = 0, pos[-1] - pos[0]
    best = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if can(mid):
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best
