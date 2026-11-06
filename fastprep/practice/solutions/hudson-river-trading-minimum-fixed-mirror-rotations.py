import sys
from typing import List

# Directions: 0=E, 1=S, 2=W, 3=N
DR = (0, 1, 0, -1)
DC = (1, 0, -1, 0)
SLASH = {0: 3, 3: 0, 1: 2, 2: 1}      # '/'
BACK = {0: 1, 1: 0, 2: 3, 3: 2}       # '\'


def minimumMirrorRotations(grid: List[str]) -> int:
    sys.setrecursionlimit(10000)
    R, C = len(grid), len(grid[0])
    INF = float("inf")
    best = [INF]
    orient = {}  # (r, c) -> chosen char, fixed once the beam first meets it

    def walk(r, c, d, cost, seen):
        # Follow the beam from cell (r, c) entered moving d.
        while True:
            if cost >= best[0]:
                return
            if not (0 <= r < R and 0 <= c < C):
                return
            ch = grid[r][c]
            if ch != '.':
                if (r, c) not in orient:
                    for choice in ('/', '\\'):
                        extra = 0 if choice == ch else 1
                        orient[(r, c)] = choice
                        walk(r, c, d, cost + extra, set(seen))
                        del orient[(r, c)]
                    return
                ch = orient[(r, c)]
                d = SLASH[d] if ch == '/' else BACK[d]
            state = (r, c, d)
            if state in seen:
                return  # beam loops forever
            seen.add(state)
            nr, nc = r + DR[d], c + DC[d]
            if not (0 <= nr < R and 0 <= nc < C):
                if r == R - 1 and c == C - 1 and d in (0, 1):
                    best[0] = cost
                return
            r, c = nr, nc

    walk(0, 0, 0, 0, set())
    return -1 if best[0] == INF else best[0]
