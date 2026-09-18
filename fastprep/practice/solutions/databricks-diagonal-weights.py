# Simulation: trace each bouncing diagonal path, then sort (weight, leftmost value) pairs.
from typing import List, Optional, Any


def Diagonalweights(matrix: List[List[int]]) -> List[int]:
    n = len(matrix)
    if n == 0:
        return []
    m = len(matrix[0])
    pairs = []
    for start in range(n):
        r = start
        d = -1
        total = matrix[r][0]
        for c in range(1, m):
            if d == -1 and r == 0:
                d = 1
            elif d == 1 and r == n - 1:
                d = -1
            r += d
            total += matrix[r][c]
        pairs.append((total, matrix[start][0]))
    pairs.sort()
    return [p[1] for p in pairs]
