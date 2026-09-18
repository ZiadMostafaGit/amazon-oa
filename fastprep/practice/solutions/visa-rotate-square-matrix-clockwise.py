# Build a new matrix where result[r][c] = matrix[n-1-c][r] (90 degree clockwise rotation).
from typing import List


def rotateSquareMatrixClockwise(matrix: List[List[int]]) -> List[List[int]]:
    n = len(matrix)
    return [[matrix[n - 1 - c][r] for c in range(n)] for r in range(n)]
