# Greedy: sort costs ascending, prefix sums; compare the type-0-only plan against
# paying the cooler fee and forcing the cheapest type-1 item into the k cheapest.
from typing import List, Optional, Any


def maxPurchasableItems(costs: List[int], types: List[int], budget: int, coolerCost: int) -> int:
    n = len(costs)
    best = 0

    # Plan A: buy only type-0 items, no cooler fee.
    zeros = sorted(c for c, t in zip(costs, types) if t == 0)
    spent = 0
    for i, c in enumerate(zeros):
        spent += c
        if spent <= budget:
            best = i + 1
        else:
            break

    # Plan B: pay the cooler fee once and buy at least one type-1 item.
    ones = [c for c, t in zip(costs, types) if t == 1]
    if not ones:
        return best
    remaining = budget - coolerCost
    if remaining < 0:
        return best
    cheapest_one = min(ones)

    items = sorted(zip(costs, types))
    prefix = 0
    ones_seen = 0
    for k in range(1, n + 1):
        c, t = items[k - 1]
        prefix += c
        if t == 1:
            ones_seen += 1
        if ones_seen > 0:
            need = prefix
        else:
            # All k cheapest are type-0: swap the priciest of them for the cheapest type-1.
            need = prefix - c + cheapest_one
        if need <= remaining and k > best:
            best = k
    return best
