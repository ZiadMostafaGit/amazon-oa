from typing import List, Optional, Any
from itertools import permutations


def _vis(seq):
    best, cnt = 0, 0
    for h in seq:
        if h > best:
            best, cnt = h, cnt + 1
    return cnt


def solveBoundaryGrid(clues: List[List[int]]) -> List[List[int]]:
    top, right, bottom, left = clues
    perms = sorted(permutations(range(1, 5)))
    rows_ok = []
    for r in range(4):
        rows_ok.append([p for p in perms
                        if (left[r] == 0 or _vis(p) == left[r])
                        and (right[r] == 0 or _vis(p[::-1]) == right[r])])
    grid = []

    def col_ok(final):
        for c in range(4):
            col = [grid[r][c] for r in range(len(grid))]
            if len(set(col)) != len(col):
                return False
            if final:
                if top[c] and _vis(col) != top[c]:
                    return False
                if bottom[c] and _vis(col[::-1]) != bottom[c]:
                    return False
        return True

    def bt(r):
        if r == 4:
            return True
        for p in rows_ok[r]:
            grid.append(p)
            if col_ok(r == 3) and bt(r + 1):
                return True
            grid.pop()
        return False

    if bt(0):
        return [list(p) for p in grid]
    return []
