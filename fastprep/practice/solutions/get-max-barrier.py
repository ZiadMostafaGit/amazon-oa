# Binary search on the barrier; evaluate the clipped sum with a sorted prefix-sum array.
from typing import List, Optional, Any
from bisect import bisect_right


def getMaxBarrier(initialEnergy: List[int], th: int) -> int:
    energies = sorted(initialEnergy)
    n = len(energies)
    prefix = [0] * (n + 1)
    for i, e in enumerate(energies):
        prefix[i + 1] = prefix[i] + e

    def remaining(barrier: int) -> int:
        idx = bisect_right(energies, barrier)
        return (prefix[n] - prefix[idx]) - barrier * (n - idx)

    lo, hi = 0, energies[-1] if n else 0
    best = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if remaining(mid) >= th:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best
