# Bottom-up DP from destination: dp[i][j] = minimum health needed on entering cell (i,j).
from typing import List, Optional, Any


def calculateMinimumHP(dungeon: List[List[int]]) -> int:
    m = len(dungeon)
    n = len(dungeon[0])
    INF = float('inf')
    # dp over rows, dp[j] = min health required upon entering cell (i, j)
    dp = [INF] * (n + 1)
    dp[n - 1] = 1  # sentinel so that the destination needs >= 1 after its own value
    for i in range(m - 1, -1, -1):
        new = [INF] * (n + 1)
        for j in range(n - 1, -1, -1):
            need = min(dp[j], new[j + 1]) - dungeon[i][j]
            new[j] = need if need > 1 else 1
        dp = new
        dp[n] = INF
    return dp[0]
