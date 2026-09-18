# BFS over stopping cells: from each stop, roll in all four directions until a wall.
from typing import List, Optional, Any
from collections import deque


def hasPath(maze: List[List[int]], start: List[int], destination: List[int]) -> bool:
    rows, cols = len(maze), len(maze[0])
    dest = (destination[0], destination[1])
    src = (start[0], start[1])
    if src == dest:
        return True
    seen = {src}
    q = deque([src])
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r, c
            while 0 <= nr + dr < rows and 0 <= nc + dc < cols and maze[nr + dr][nc + dc] == 0:
                nr += dr
                nc += dc
            if (nr, nc) == dest:
                return True
            if (nr, nc) not in seen:
                seen.add((nr, nc))
                q.append((nr, nc))
    return False
