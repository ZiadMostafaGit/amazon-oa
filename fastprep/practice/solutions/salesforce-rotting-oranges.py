# Multi-source BFS from every initially rotten orange, counting layers.
from collections import deque
from typing import List, Optional, Any


def orangesRotting(grid: List[List[int]]) -> int:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    q = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1
    if fresh == 0:
        return 0
    seen = [[cell == 2 for cell in row] for row in grid]
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
    return minutes if fresh == 0 else -1
