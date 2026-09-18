# Bottom-up unbounded-knapsack DP over amounts 0..amount.
from typing import List


def coinChange(coins: List[int], amount: int) -> int:
    INF = float('inf')
    dp = [0] + [INF] * amount
    for value in range(1, amount + 1):
        best = INF
        for coin in coins:
            if coin <= value:
                prev = dp[value - coin]
                if prev + 1 < best:
                    best = prev + 1
        dp[value] = best
    return -1 if dp[amount] == INF else dp[amount]
