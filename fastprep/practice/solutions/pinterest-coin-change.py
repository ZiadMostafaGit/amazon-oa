# Bottom-up unbounded-knapsack DP over amounts 0..amount.
from typing import List, Optional, Any


def coinChange(coins: List[int], amount: int) -> int:
    if amount == 0:
        return 0
    INF = amount + 1
    dp = [0] + [INF] * amount
    usable = [c for c in coins if 0 < c <= amount]
    for c in usable:
        for a in range(c, amount + 1):
            cand = dp[a - c] + 1
            if cand < dp[a]:
                dp[a] = cand
    return -1 if dp[amount] >= INF else dp[amount]
