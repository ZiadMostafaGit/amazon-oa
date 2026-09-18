from typing import List, Optional, Any
from collections import deque


def longestIncreasingPath(matrix: List[List[int]]) -> int:
    if not matrix or not matrix[0]:
        return 0
    rows = len(matrix)
    cols = len(matrix[0])

    # Edge u -> v when matrix[v] > matrix[u]. Peel cells with no incoming edge
    # (no strictly smaller neighbour) layer by layer: the number of layers is
    # the longest strictly increasing path.
    outdeg = [[0] * cols for _ in range(rows)]
    queue = deque()
    for r in range(rows):
        row = matrix[r]
        for c in range(cols):
            v = row[c]
            d = 0
            if r > 0 and matrix[r - 1][c] > v:
                d += 1
            if r + 1 < rows and matrix[r + 1][c] > v:
                d += 1
            if c > 0 and row[c - 1] > v:
                d += 1
            if c + 1 < cols and row[c + 1] > v:
                d += 1
            outdeg[r][c] = d
            if d == 0:
                queue.append((r, c))

    layers = 0
    while queue:
        layers += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            v = matrix[r][c]
            for nr, nc in ((r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)):
                if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] < v:
                    outdeg[nr][nc] -= 1
                    if outdeg[nr][nc] == 0:
                        queue.append((nr, nc))
    return layers
