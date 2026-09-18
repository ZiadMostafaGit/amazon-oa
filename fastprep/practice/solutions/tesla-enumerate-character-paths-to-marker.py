# DFS with a visited set collecting characters, then sort the resulting strings lexicographically.
from typing import List, Optional, Any


def enumeratePaths(grid: List[List[str]]) -> List[str]:
    rows = len(grid)
    cols = len(grid[0])
    results = []
    visited = [[False] * cols for _ in range(rows)]
    path = []

    def dfs(r: int, c: int) -> None:
        if grid[r][c] == "*":
            results.append("".join(path))
            return
        visited[r][c] = True
        path.append(grid[r][c])
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and not visited[nr][nc]:
                dfs(nr, nc)
        path.pop()
        visited[r][c] = False

    dfs(0, 0)
    results.sort()
    return results
