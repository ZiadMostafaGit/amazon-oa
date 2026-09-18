# BFS for the shortest path on the grid, then compare its length with maxTime.
from collections import deque
from typing import List


def reachTheEnd(grid: List[str], maxTime: int) -> str:
    n = len(grid)
    m = len(grid[0]) if n else 0
    if n == 0 or m == 0:
        return "No"
    if grid[0][0] == '#' or grid[n - 1][m - 1] == '#':
        return "No"
    if n == 1 and m == 1:
        return "Yes" if maxTime >= 0 else "No"

    dist = [[-1] * m for _ in range(n)]
    dist[0][0] = 0
    q = deque([(0, 0)])
    while q:
        r, c = q.popleft()
        d = dist[r][c]
        if d >= maxTime:
            continue
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < n and 0 <= nc < m and dist[nr][nc] == -1 and grid[nr][nc] != '#':
                dist[nr][nc] = d + 1
                if nr == n - 1 and nc == m - 1:
                    return "Yes"
                q.append((nr, nc))
    return "No"
