# DP: dp[j] = side of largest all-'1' square ending at this cell, rolled over one row.
from typing import List, Optional, Any


def maximalSquare(matrix: List[List[str]]) -> int:
    if not matrix or not matrix[0]:
        return 0
    n = len(matrix[0])
    prev = [0] * (n + 1)
    best = 0
    for row in matrix:
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            if row[j - 1] == '1':
                cur[j] = min(prev[j], prev[j - 1], cur[j - 1]) + 1
                if cur[j] > best:
                    best = cur[j]
        prev = cur
    return best * best
