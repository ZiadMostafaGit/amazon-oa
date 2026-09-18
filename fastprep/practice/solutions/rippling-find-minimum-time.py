# Binary search on the number of processes per processor, with a greedy largest-process-to-largest-capacity feasibility check.
from typing import List, Optional, Any


def findMinimumTime(processSize: List[int], capacity: List[int]) -> int:
    n = len(processSize)
    if n == 0:
        return 0
    if not capacity or max(processSize) > max(capacity):
        return -1
    procs = sorted(processSize, reverse=True)
    caps = sorted(capacity, reverse=True)

    def feasible(k: int) -> bool:
        j = 0
        for cap in caps:
            if j >= n:
                return True
            if procs[j] > cap:
                return False
            taken = 0
            while taken < k and j < n and procs[j] <= cap:
                j += 1
                taken += 1
        return j >= n

    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid
        else:
            lo = mid + 1
    return 2 * lo - 1
