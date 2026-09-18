# Peel concentric layers, collect each border's clockwise coordinates, sort the values, write them back.
from typing import List, Optional, Any


def sortMatrixBorders(matrix: List[List[int]]) -> List[List[int]]:
    if not matrix or not matrix[0]:
        return matrix
    rows = len(matrix)
    cols = len(matrix[0])
    top, bottom, left, right = 0, rows - 1, 0, cols - 1
    while top <= bottom and left <= right:
        coords = []
        if top == bottom:
            for c in range(left, right + 1):
                coords.append((top, c))
        elif left == right:
            for r in range(top, bottom + 1):
                coords.append((r, left))
        else:
            for c in range(left, right + 1):
                coords.append((top, c))
            for r in range(top + 1, bottom + 1):
                coords.append((r, right))
            for c in range(right - 1, left - 1, -1):
                coords.append((bottom, c))
            for r in range(bottom - 1, top, -1):
                coords.append((r, left))
        values = sorted(matrix[r][c] for r, c in coords)
        for (r, c), v in zip(coords, values):
            matrix[r][c] = v
        top += 1
        bottom -= 1
        left += 1
        right -= 1
    return matrix
