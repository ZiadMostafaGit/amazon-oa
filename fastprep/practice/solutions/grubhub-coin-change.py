# Bottom-up unbounded-knapsack DP over amounts 0..amount.
from typing import List, Optional, Any


def coinChange(coins: List[int], amount: int) -> int:
    INF = float('inf')
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        best = INF
        for c in coins:
            if c <= a:
                prev = dp[a - c]
                if prev + 1 < best:
                    best = prev + 1
        dp[a] = best
    return -1 if dp[amount] == INF else dp[amount]
