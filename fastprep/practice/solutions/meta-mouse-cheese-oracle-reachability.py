# BFS flood fill over open cells from (0, 0) to test reachability of the cheese cell.
from collections import deque
from typing import List, Optional, Any


def canReachCheese(grid: List[str]) -> bool:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if rows == 0 or cols == 0:
        return False
    if grid[0][0] == '#':
        return False
    seen = [[False] * cols for _ in range(rows)]
    seen[0][0] = True
    queue = deque([(0, 0)])
    while queue:
        r, c = queue.popleft()
        if grid[r][c] == 'C':
            return True
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and not seen[nr][nc] and grid[nr][nc] != '#':
                seen[nr][nc] = True
                queue.append((nr, nc))
    return False
