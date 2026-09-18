# Simulate the walk on a row/col grid, checking each visited cell against an obstacle set.
from typing import List, Optional, Any


def returnsSafely(moves: str, obstacles: List[List[int]]) -> bool:
    blocked = {(int(o[0]), int(o[1])) for o in obstacles}
    r = c = 0
    step = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
    for ch in moves:
        dr, dc = step[ch]
        r += dr
        c += dc
        if (r, c) in blocked:
            return False
    return r == 0 and c == 0
