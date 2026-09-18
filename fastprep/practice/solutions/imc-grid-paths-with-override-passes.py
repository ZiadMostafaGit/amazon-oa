# Grid DP over (row, col, overrides used) counting paths mod 1e9+7.
from typing import List, Optional, Any


def numPaths(grid: List[List[int]], k: int) -> int:
    MOD = 10 ** 9 + 7
    n = len(grid)
    m = len(grid[0]) if n else 0
    if n == 0 or m == 0:
        return 0

    # dp[j][u] = ways to reach current cell (i, j) having used u overrides
    dp = [[0] * (k + 1) for _ in range(m)]

    for i in range(n):
        for j in range(m):
            cost = 0 if grid[i][j] == 1 else 1
            if i == 0 and j == 0:
                cur = [0] * (k + 1)
                if cost <= k:
                    cur[cost] = 1
                dp[j] = cur
                continue
            # incoming = from top (dp[j], previous row) + from left (dp[j-1], current row)
            inc = [0] * (k + 1)
            if i > 0:
                top = dp[j]
                for u in range(k + 1):
                    if top[u]:
                        inc[u] = (inc[u] + top[u]) % MOD
            if j > 0:
                left = dp[j - 1]
                for u in range(k + 1):
                    if left[u]:
                        inc[u] = (inc[u] + left[u]) % MOD
            cur = [0] * (k + 1)
            if cost == 0:
                cur = inc
            else:
                for u in range(k):
                    if inc[u]:
                        cur[u + 1] = inc[u]
            dp[j] = cur

    return sum(dp[m - 1]) % MOD
