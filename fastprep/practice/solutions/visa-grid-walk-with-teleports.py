# Deterministic simulation of the walk with a visited-cell set for cycle detection.
from typing import List, Optional, Any


def solution(n: int, m: int, obstacles: List[List[int]], teleports: List[List[int]]) -> int:
    blocked = set()
    for cell in obstacles:
        blocked.add((cell[0], cell[1]))

    portal = {}
    for t in teleports:
        portal[(t[0], t[1])] = (t[2], t[3])

    goal = (n - 1, m - 1)
    cur = (0, 0)
    count = 1
    seen = {cur}

    while True:
        if cur == goal:
            return count

        if cur in portal:
            nxt = portal[cur]
        else:
            r, c = cur
            if c + 1 < m and (r, c + 1) not in blocked:
                nxt = (r, c + 1)
            elif r + 1 < n and (r + 1, c) not in blocked:
                nxt = (r + 1, c)
            else:
                return -1

        count += 1
        if nxt in seen:
            return -2
        seen.add(nxt)
        cur = nxt
