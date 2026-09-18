# Staircase (Young tableau) search starting from the top-right corner.
from typing import List, Optional, Any


def staircaseSearch(matrix: List[List[int]], target: int) -> bool:
    if not matrix or not matrix[0]:
        return False
    row = 0
    col = len(matrix[0]) - 1
    while row < len(matrix) and col >= 0:
        value = matrix[row][col]
        if value == target:
            return True
        if value > target:
            col -= 1
        else:
            row += 1
    return False
