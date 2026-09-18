# Walk each concentric ring clockwise, sort its values, and write them back in traversal order.
from typing import List, Optional, Any


def solution(matrix: List[List[int]]) -> List[List[int]]:
    n = len(matrix)
    m = len(matrix[0])
    res = [row[:] for row in matrix]
    top, bottom, left, right = 0, n - 1, 0, m - 1
    while top <= bottom and left <= right:
        coords = []
        for c in range(left, right + 1):
            coords.append((top, c))
        for r in range(top + 1, bottom + 1):
            coords.append((r, right))
        if bottom > top:
            for c in range(right - 1, left - 1, -1):
                coords.append((bottom, c))
        if right > left:
            for r in range(bottom - 1, top, -1):
                coords.append((r, left))
        values = sorted(res[r][c] for r, c in coords)
        for (r, c), v in zip(coords, values):
            res[r][c] = v
        top += 1
        bottom -= 1
        left += 1
        right -= 1
    return res
