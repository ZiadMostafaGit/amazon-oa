# Direct simulation of the bouncing diagonal walk, stopping at a corner or a revisited cell.
from typing import List, Optional, Any


def solution(matrix: List[List[int]], cellX: int, cellY: int) -> int:
    n = len(matrix)
    m = len(matrix[0])
    corners = {(0, 0), (0, m - 1), (n - 1, 0), (n - 1, m - 1)}

    x, y = cellX, cellY
    dx, dy = 1, 1
    visited = {(x, y)}
    total = matrix[x][y]

    while True:
        if not (0 <= x + dx < n):
            dx = -dx
        if not (0 <= y + dy < m):
            dy = -dy
        x += dx
        y += dy
        if (x, y) in visited:
            break
        visited.add((x, y))
        total += matrix[x][y]
        if (x, y) in corners:
            break
    return total
