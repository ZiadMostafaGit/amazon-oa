# 0/1 knapsack dynamic programming over the budget dimension.
from typing import List, Optional, Any


def maximizeProjectValue(costs: List[int], values: List[int], budget: int) -> int:
    dp = [0] * (budget + 1)
    for c, v in zip(costs, values):
        if c > budget:
            continue
        for b in range(budget, c - 1, -1):
            cand = dp[b - c] + v
            if cand > dp[b]:
                dp[b] = cand
    return max(dp) if dp else 0
