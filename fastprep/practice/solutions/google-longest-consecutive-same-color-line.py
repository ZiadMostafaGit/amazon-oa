# Dynamic programming over four directions: run length ending at each cell per orientation.
from typing import List, Optional, Any


def longestSameColorLine(grid: List[str]) -> int:
    if not grid:
        return 0
    m = len(grid)
    n = len(grid[0]) if m else 0
    if n == 0:
        return 0

    # dp[d][j] for the current row, d in {right, down, down-right, down-left}
    prev = [[0] * n for _ in range(4)]
    best = 0
    for i in range(m):
        row = grid[i]
        cur = [[0] * n for _ in range(4)]
        for j in range(n):
            c = row[j]
            # horizontal (left to right)
            cur[0][j] = cur[0][j - 1] + 1 if j > 0 and row[j - 1] == c else 1
            # vertical (top to bottom)
            cur[1][j] = prev[1][j] + 1 if i > 0 and grid[i - 1][j] == c else 1
            # diagonal down-right: previous cell is (i-1, j-1)
            cur[2][j] = prev[2][j - 1] + 1 if i > 0 and j > 0 and grid[i - 1][j - 1] == c else 1
            # diagonal down-left: previous cell is (i-1, j+1)
            cur[3][j] = prev[3][j + 1] + 1 if i > 0 and j + 1 < n and grid[i - 1][j + 1] == c else 1
            for d in range(4):
                if cur[d][j] > best:
                    best = cur[d][j]
        prev = cur
    return best
