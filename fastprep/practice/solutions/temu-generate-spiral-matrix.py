# Boundary shrinking: fill top row, right column, bottom row, left column, then move inward.
from typing import List, Optional, Any


def generateMatrix(n: int) -> List[List[int]]:
    grid = [[0] * n for _ in range(n)]
    top, bottom, left, right = 0, n - 1, 0, n - 1
    v = 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            grid[top][c] = v
            v += 1
        top += 1
        for r in range(top, bottom + 1):
            grid[r][right] = v
            v += 1
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                grid[bottom][c] = v
                v += 1
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                grid[r][left] = v
                v += 1
            left += 1
    return grid
