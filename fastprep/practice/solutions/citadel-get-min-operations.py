# Binary search on the op count; a run of m ops works iff sum of needed major-picks <= m.
from typing import List


def citadelGetMinOperations(executionTime: List[int], x: int, y: int) -> int:
    ts = sorted(executionTime, reverse=True)
    n = len(ts)
    d = x - y

    def feasible(m: int) -> bool:
        base = m * y
        total = 0
        for t in ts:
            if t <= base:
                break
            total += (t - base + d - 1) // d
            if total > m:
                return False
        return True

    lo, hi = 1, (ts[0] + y - 1) // y
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo
