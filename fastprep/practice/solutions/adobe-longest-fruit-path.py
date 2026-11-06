from typing import List


def longestFruitPath(grid: List[List[int]]) -> int:
    if not grid or not grid[0]:
        return 0
    r, c = len(grid), len(grid[0])
    seen = [[False] * c for _ in range(r)]
    best = 0

    def dfs(i, j, length):
        nonlocal best
        if length > best:
            best = length
        seen[i][j] = True
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = i + di, j + dj
            if 0 <= a < r and 0 <= b < c and grid[a][b] == 1 and not seen[a][b]:
                dfs(a, b, length + 1)
        seen[i][j] = False

    for i in range(r):
        for j in range(c):
            if grid[i][j] == 1:
                dfs(i, j, 1)
    return best
