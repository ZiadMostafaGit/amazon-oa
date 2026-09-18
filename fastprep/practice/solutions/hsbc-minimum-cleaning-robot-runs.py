# Iterative BFS flood fill over non-wall cells; count connected rooms that contain at least one dirty field.
from typing import List, Optional, Any
from collections import deque


def solution(plan: List[str]) -> int:
    if not plan or not plan[0]:
        return 0
    rows = len(plan)
    cols = len(plan[0])
    seen = [[False] * cols for _ in range(rows)]
    runs = 0
    for r in range(rows):
        row = plan[r]
        for c in range(cols):
            if row[c] == '#' or seen[r][c]:
                continue
            seen[r][c] = True
            q = deque([(r, c)])
            dirty = False
            while q:
                y, x = q.popleft()
                if plan[y][x] == '*':
                    dirty = True
                if y > 0 and not seen[y - 1][x] and plan[y - 1][x] != '#':
                    seen[y - 1][x] = True
                    q.append((y - 1, x))
                if y + 1 < rows and not seen[y + 1][x] and plan[y + 1][x] != '#':
                    seen[y + 1][x] = True
                    q.append((y + 1, x))
                if x > 0 and not seen[y][x - 1] and plan[y][x - 1] != '#':
                    seen[y][x - 1] = True
                    q.append((y, x - 1))
                if x + 1 < cols and not seen[y][x + 1] and plan[y][x + 1] != '#':
                    seen[y][x + 1] = True
                    q.append((y, x + 1))
            if dirty:
                runs += 1
    return runs
