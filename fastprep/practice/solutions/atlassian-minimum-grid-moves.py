# BFS over cells where each move slides 1..k cells in one direction, stopping at obstacles.
from typing import List, Optional, Any
from collections import deque


def getMinimumMoves(maze: List[List[int]], k: int) -> int:
    rows = len(maze)
    cols = len(maze[0]) if rows else 0
    if rows == 0 or cols == 0:
        return -1
    if maze[0][0] == 1 or maze[rows - 1][cols - 1] == 1:
        return -1
    if rows == 1 and cols == 1:
        return 0
    dist = [[-1] * cols for _ in range(rows)]
    dist[0][0] = 0
    q = deque([(0, 0)])
    while q:
        r, c = q.popleft()
        d = dist[r][c]
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r, c
            for _ in range(k):
                nr += dr
                nc += dc
                if nr < 0 or nr >= rows or nc < 0 or nc >= cols:
                    break
                if maze[nr][nc] == 1:
                    break
                if dist[nr][nc] == -1:
                    dist[nr][nc] = d + 1
                    if nr == rows - 1 and nc == cols - 1:
                        return d + 1
                    q.append((nr, nc))
    return dist[rows - 1][cols - 1]
