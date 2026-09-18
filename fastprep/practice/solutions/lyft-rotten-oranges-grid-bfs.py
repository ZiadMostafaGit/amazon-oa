# Multi-source BFS level by level from all infected cells, one level per minute.
from typing import List, Optional, Any
from collections import deque


def minimumMinutesToInfectAll(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    q = deque()
    fresh = 0
    seen = [[False] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c))
                seen[r][c] = True
            elif grid[r][c] == 1:
                fresh += 1

    if fresh == 0:
        return 0

    minutes = 0
    while q and fresh:
        minutes += 1
        for _ in range(len(q)):
            r, c = q.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc] and grid[nr][nc] == 1:
                    seen[nr][nc] = True
                    fresh -= 1
                    q.append((nr, nc))

    return -1 if fresh else minutes
