# Direct simulation of the bouncing diagonal walk with a visited set as the stopping condition.
from typing import List, Optional, Any


def solution(matrix: List[List[int]], cellX: int, cellY: int) -> int:
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    corners = {(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)}

    r, c = cellX, cellY
    dr, dc = 1, 1
    total = matrix[r][c]
    visited = {(r, c)}

    while True:
        if not (0 <= r + dr < rows):
            dr = -dr
        if not (0 <= c + dc < cols):
            dc = -dc
        r += dr
        c += dc
        if (r, c) in visited:
            break
        total += matrix[r][c]
        if (r, c) in corners:
            break
        visited.add((r, c))
    return total
