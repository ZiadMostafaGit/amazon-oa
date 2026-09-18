# Precompute each row's maximum and each column's minimum, then scan for a cell that is both.
from typing import List, Optional, Any


def findElementLargestInRowSmallestInColumn(matrix: List[List[int]]) -> int:
    if not matrix or not matrix[0]:
        return -1
    rows = len(matrix)
    cols = len(matrix[0])
    row_max = [max(r) for r in matrix]
    col_min = [min(matrix[i][j] for i in range(rows)) for j in range(cols)]
    for i in range(rows):
        mx = row_max[i]
        row = matrix[i]
        for j in range(cols):
            if row[j] == mx and row[j] == col_min[j]:
                return row[j]
    return -1
