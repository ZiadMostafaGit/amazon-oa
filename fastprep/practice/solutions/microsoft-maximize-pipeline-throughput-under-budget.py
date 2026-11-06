# Binary search the target throughput T: reaching T costs sum((ceil(T / t) - 1) * c), which only grows with T.
from typing import List, Optional, Any


def maximizePipelineThroughput(throughput: List[int], scalingCost: List[int], budget: int) -> int:
    def cost(T: int) -> int:
        total = 0
        for t, c in zip(throughput, scalingCost):
            steps = (T + t - 1) // t - 1
            if steps > 0:
                total += steps * c
                if total > budget:
                    return total
        return total

    lo = min(throughput)  # always reachable for free
    hi = min(t * (budget // c + 1) for t, c in zip(throughput, scalingCost))
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if cost(mid) <= budget:
            lo = mid
        else:
            hi = mid - 1
    return lo
