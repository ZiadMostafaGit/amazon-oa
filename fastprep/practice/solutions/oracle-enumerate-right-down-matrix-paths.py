# Reachability DP to prune, then DFS emitting 'D' before 'R' for lexicographic order.
from typing import List, Optional, Any


def enumeratePaths(grid: List[List[int]]) -> List[str]:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if rows == 0 or cols == 0:
        return []
    if grid[0][0] != 1 or grid[rows - 1][cols - 1] != 1:
        return []

    reach = [[False] * cols for _ in range(rows)]
    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            if grid[r][c] != 1:
                continue
            if r == rows - 1 and c == cols - 1:
                reach[r][c] = True
            else:
                down = reach[r + 1][c] if r + 1 < rows else False
                right = reach[r][c + 1] if c + 1 < cols else False
                reach[r][c] = down or right
    if not reach[0][0]:
        return []

    out: List[str] = []
    path: List[str] = []

    def dfs(r: int, c: int) -> None:
        if r == rows - 1 and c == cols - 1:
            out.append("".join(path))
            return
        if r + 1 < rows and reach[r + 1][c]:
            path.append('D')
            dfs(r + 1, c)
            path.pop()
        if c + 1 < cols and reach[r][c + 1]:
            path.append('R')
            dfs(r, c + 1)
            path.pop()

    import sys
    sys.setrecursionlimit(10000 + rows + cols + 100)
    dfs(0, 0)
    return out
