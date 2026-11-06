# Treat the matrix as one sorted array of rows*cols cells: cell k is matrix[k // cols][k % cols].
from typing import List, Optional, Any


def searchMatrix(matrix: List[List[int]], target: int) -> bool:
    if not matrix or not matrix[0]:
        return False
    rows, cols = len(matrix), len(matrix[0])
    lo, hi = 0, rows * cols - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        v = matrix[mid // cols][mid % cols]
        if v == target:
            return True
        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return False
