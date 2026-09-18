# Any p pair-buys can cover exactly the 2p most expensive books (cut between the p-th and (p+1)-th of them),
# so just maximise (sum of 2p largest - p*pairCost) over p.
from typing import List, Optional, Any


def getMinCost(cost: List[int], pairCost: int, k: int) -> int:
    n = len(cost)
    total = sum(cost)
    desc = sorted(cost, reverse=True)

    best_saving = 0
    running = 0
    limit = min(k, n // 2)
    for p in range(1, limit + 1):
        running += desc[2 * p - 2] + desc[2 * p - 1]
        saving = running - p * pairCost
        if saving > best_saving:
            best_saving = saving
    return total - best_saving
