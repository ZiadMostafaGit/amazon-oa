# DP: dp[i][j] = largest all-ones square side ending at cell (i, j).
from typing import List, Optional, Any


def largestSquare(matrix: List[List[int]]) -> int:
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    prev = [0] * cols
    best = 0
    for i in range(rows):
        cur = [0] * cols
        for j in range(cols):
            if matrix[i][j] == 1:
                if i == 0 or j == 0:
                    cur[j] = 1
                else:
                    cur[j] = 1 + min(prev[j], cur[j - 1], prev[j - 1])
                if cur[j] > best:
                    best = cur[j]
        prev = cur
    return best
