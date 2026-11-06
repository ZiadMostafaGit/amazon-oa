# Binary search the number of units u: buying for u units costs sum(max(0, u*comp - stock) * cost), monotone in u.
from typing import List, Optional, Any


def maxAlloyUnits(composition: List[int], stock: List[int], cost: List[int], budget: int) -> int:
    def spend(u: int) -> int:
        total = 0
        for c, s, p in zip(composition, stock, cost):
            need = u * c - s
            if need > 0:
                total += need * p
                if total > budget:
                    return total
        return total

    lo = 0
    hi = min((s + budget // p) // c for c, s, p in zip(composition, stock, cost))
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if spend(mid) <= budget:
            lo = mid
        else:
            hi = mid - 1
    return lo
