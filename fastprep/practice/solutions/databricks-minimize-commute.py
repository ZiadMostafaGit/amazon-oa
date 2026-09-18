# BFS per transport mode over the grid, then pick min (steps*time, steps*cost).
from typing import List, Optional, Any
from collections import deque


def minimizeCommute(grid: List[List[str]], time: List[int], cost: List[int]) -> str:
    names = ["Walk", "Bike", "Car", "Train"]
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    start = end = None
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 'S':
                start = (r, c)
            elif grid[r][c] == 'D':
                end = (r, c)

    best = None
    best_name = ""
    for m in range(4):
        label = str(m + 1)
        dist = [[-1] * cols for _ in range(rows)]
        dist[start[0]][start[1]] = 0
        q = deque([start])
        found = -1
        while q:
            r, c = q.popleft()
            if (r, c) == end:
                found = dist[r][c]
                break
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                    ch = grid[nr][nc]
                    if ch == label or ch == 'D' or ch == 'S':
                        dist[nr][nc] = dist[r][c] + 1
                        q.append((nr, nc))
        if found < 0:
            continue
        key = (found * time[m], found * cost[m])
        if best is None or key < best:
            best = key
            best_name = names[m]
    return best_name
