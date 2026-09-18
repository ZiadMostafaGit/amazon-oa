# Approach: in-place transpose followed by reversing each row.
from typing import List, Optional, Any


def rotateImage(matrix: List[List[int]]) -> List[List[int]]:
    n = len(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]
    for row in matrix:
        row.reverse()
    return matrix
