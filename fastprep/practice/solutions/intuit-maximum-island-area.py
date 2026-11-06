from typing import List, Optional, Any


def maxAreaOfIsland(grid: List[List[int]]) -> int:
    rows, cols = len(grid), len(grid[0]) if grid else 0
    seen = [[False] * cols for _ in range(rows)]
    best = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 1 or seen[r][c]:
                continue
            seen[r][c] = True
            stack = [(r, c)]
            area = 0
            while stack:
                y, x = stack.pop()
                area += 1
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == 1 and not seen[ny][nx]:
                        seen[ny][nx] = True
                        stack.append((ny, nx))
            best = max(best, area)
    return best
