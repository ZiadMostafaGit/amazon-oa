# BFS over grid cells, expanding up to k steps in each direction and stopping at the first obstacle.
from typing import List, Optional, Any
from collections import deque


def getMinimumMoves(maze: List[List[int]], k: int) -> int:
    n = len(maze)
    m = len(maze[0])
    if maze[0][0] == 1 or maze[n - 1][m - 1] == 1:
        return -1
    if n == 1 and m == 1:
        return 0
    dist = [[-1] * m for _ in range(n)]
    dist[0][0] = 0
    q = deque([(0, 0)])
    while q:
        i, j = q.popleft()
        d = dist[i][j]
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i, j
            for _ in range(k):
                ni += di
                nj += dj
                if ni < 0 or ni >= n or nj < 0 or nj >= m or maze[ni][nj] == 1:
                    break
                if dist[ni][nj] == -1:
                    dist[ni][nj] = d + 1
                    if ni == n - 1 and nj == m - 1:
                        return d + 1
                    q.append((ni, nj))
    return -1
