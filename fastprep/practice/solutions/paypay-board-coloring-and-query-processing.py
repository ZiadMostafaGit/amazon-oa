# Direct grid simulation: mark cells black, scan in the requested direction for the next white cell.
from typing import List, Optional, Any


def solution(h: int, w: int, queries: List[str]) -> List[List[int]]:
    black = [[False] * w for _ in range(h)]
    res = []
    for q in queries:
        parts = q.split()
        op = parts[0]
        a = int(parts[1])
        b = int(parts[2])
        if op == 'x':
            black[a][b] = True
            continue
        if op == '>':
            step_r, step_c = 0, 1
        elif op == '<':
            step_r, step_c = 0, -1
        elif op == 'v':
            step_r, step_c = 1, 0
        else:
            step_r, step_c = -1, 0
        r, c = a + step_r, b + step_c
        found = [-1, -1]
        while 0 <= r < h and 0 <= c < w:
            if not black[r][c]:
                found = [r, c]
                break
            r += step_r
            c += step_c
        res.append(found)
    return res
