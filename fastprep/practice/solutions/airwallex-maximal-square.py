# DP: dp[i][j] = side of the largest all-ones square whose bottom-right corner is (i,j).
from typing import List, Optional, Any


def maximalSquare(matrix: List[List[str]]) -> int:
    if not matrix or not matrix[0]:
        return 0
    n = len(matrix[0])
    prev = [0] * (n + 1)
    best = 0
    for row in matrix:
        cur = [0] * (n + 1)
        for j in range(n):
            if row[j] == '1' or row[j] == 1:
                cur[j + 1] = min(prev[j + 1], cur[j], prev[j]) + 1
                if cur[j + 1] > best:
                    best = cur[j + 1]
        prev = cur
    return best * best
