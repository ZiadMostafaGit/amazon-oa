from typing import List, Optional, Any
from collections import deque


def canReachMaze(grid: List[List[int]], start: List[int], finish: List[int]) -> bool:
    R, C = len(grid), len(grid[0])
    sr, sc = start
    fr, fc = finish
    if grid[sr][sc] == 1 or grid[fr][fc] == 1:
        return False
    seen = [[False] * C for _ in range(R)]
    seen[sr][sc] = True
    q = deque([(sr, sc)])
    while q:
        r, c = q.popleft()
        if r == fr and c == fc:
            return True
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < R and 0 <= nc < C and not seen[nr][nc] and grid[nr][nc] == 0:
                seen[nr][nc] = True
                q.append((nr, nc))
    return False
