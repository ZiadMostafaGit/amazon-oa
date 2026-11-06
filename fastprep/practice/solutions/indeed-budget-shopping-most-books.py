# Unbounded knapsack, "at most n dollars": best[b] starts at 0 for every budget (unused money allowed).
from typing import List


def budgetShopping(n: int, bundleQuantities: List[int], bundleCosts: List[int]) -> int:
    best = [0] * (n + 1)
    for q, c in zip(bundleQuantities, bundleCosts):
        for b in range(c, n + 1):         # upward: a bundle may be bought again
            if best[b - c] + q > best[b]:
                best[b] = best[b - c] + q
    return best[n]
