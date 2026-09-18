# Interval DP on the score difference: dp[i][j] = best (current player - opponent) on coins[i..j].
from typing import List, Optional, Any


def firstPlayerWins(coins: List[int]) -> bool:
    n = len(coins)
    dp = [[0] * n for _ in range(n)]
    for i in range(n):
        dp[i][i] = coins[i]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(coins[i] - dp[i + 1][j], coins[j] - dp[i][j - 1])
    return dp[0][n - 1] >= 0
