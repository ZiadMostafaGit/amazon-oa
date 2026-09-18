# Dynamic programming over a single rolling row of minimum path sums.
from typing import List, Optional, Any


def minimumPathSum(grid: List[List[int]]) -> int:
    rows = len(grid)
    cols = len(grid[0])
    dp = [0] * cols
    dp[0] = grid[0][0]
    for c in range(1, cols):
        dp[c] = dp[c - 1] + grid[0][c]
    for r in range(1, rows):
        row = grid[r]
        dp[0] += row[0]
        for c in range(1, cols):
            prev = dp[c - 1]
            up = dp[c]
            dp[c] = (prev if prev < up else up) + row[c]
    return dp[cols - 1]
