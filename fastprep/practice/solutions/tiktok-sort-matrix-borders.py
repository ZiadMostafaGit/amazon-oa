# Peel concentric layers, collect each border's cells along the clockwise path, sort, write back.
from typing import List


def sortMatrixBorderLayers(matrix: List[List[int]]) -> List[List[int]]:
    if not matrix or not matrix[0]:
        return matrix
    m = len(matrix)
    n = len(matrix[0])
    grid = [row[:] for row in matrix]

    top, bottom, left, right = 0, m - 1, 0, n - 1
    while top <= bottom and left <= right:
        path = []
        for c in range(left, right + 1):
            path.append((top, c))
        for r in range(top + 1, bottom + 1):
            path.append((r, right))
        if bottom > top:
            for c in range(right - 1, left - 1, -1):
                path.append((bottom, c))
        if right > left:
            for r in range(bottom - 1, top, -1):
                path.append((r, left))

        vals = sorted(grid[r][c] for r, c in path)
        for (r, c), v in zip(path, vals):
            grid[r][c] = v

        top += 1
        bottom -= 1
        left += 1
        right -= 1

    return grid
