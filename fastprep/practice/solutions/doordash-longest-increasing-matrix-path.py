from typing import List, Optional, Any
from collections import deque


def longestIncreasingPath(matrix: List[List[int]]) -> int:
    rows, cols = len(matrix), len(matrix[0])
    dirs = ((1, 0), (-1, 0), (0, 1), (0, -1))
    # edge from smaller to larger neighbour; indeg = number of smaller neighbours
    indeg = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] < matrix[r][c]:
                    indeg[r][c] += 1
    layer = [(r, c) for r in range(rows) for c in range(cols) if indeg[r][c] == 0]
    length = 0
    while layer:
        length += 1
        nxt = []
        for r, c in layer:
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                    indeg[nr][nc] -= 1
                    if indeg[nr][nc] == 0:
                        nxt.append((nr, nc))
        layer = nxt
    return length
