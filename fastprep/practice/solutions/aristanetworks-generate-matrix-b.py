# 2D prefix sum: B[i][j] = A[i][j] + B[i-1][j] + B[i][j-1] - B[i-1][j-1].
from typing import List, Optional, Any


def generateMatrixB(A: List[List[int]]) -> List[List[int]]:
    if not A or not A[0]:
        return [list(row) for row in A]
    m, n = len(A), len(A[0])
    B = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            total = A[i][j]
            if i > 0:
                total += B[i - 1][j]
            if j > 0:
                total += B[i][j - 1]
            if i > 0 and j > 0:
                total -= B[i - 1][j - 1]
            B[i][j] = total
    return B
