# Multi-source BFS from every initially rotten orange, counting minute layers.
from collections import deque
from typing import List, Optional, Any


def orangesRotting(grid: List[List[int]]) -> int:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    if fresh == 0:
        return 0
    minutes = 0
    seen = [row[:] for row in grid]
    while queue and fresh:
        minutes += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                if 0 <= nr < rows and 0 <= nc < cols and seen[nr][nc] == 1:
                    seen[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
    return -1 if fresh else minutes
