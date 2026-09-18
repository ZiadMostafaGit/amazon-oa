# BFS over states (row, col, obstacles eliminated so far).
from typing import List, Optional, Any
from collections import deque


def shortestPath(grid: List[List[int]], k: int) -> int:
    m, n = len(grid), len(grid[0])
    if m == 1 and n == 1:
        return 0
    if k >= m + n - 3:
        return m + n - 2
    best = [[-1] * n for _ in range(m)]
    best[0][0] = k
    q = deque([(0, 0, k)])
    steps = 0
    while q:
        steps += 1
        for _ in range(len(q)):
            r, c, rem = q.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    nrem = rem - grid[nr][nc]
                    if nrem < 0:
                        continue
                    if nr == m - 1 and nc == n - 1:
                        return steps
                    if best[nr][nc] >= nrem:
                        continue
                    best[nr][nc] = nrem
                    q.append((nr, nc, nrem))
    return -1
