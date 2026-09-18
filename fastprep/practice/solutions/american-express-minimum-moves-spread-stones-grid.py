# Min-cost assignment of surplus stones to empty cells by Manhattan distance (brute-force permutations).
from itertools import permutations
from typing import List, Optional, Any


def minimumMovesToSpreadStones(grid: List[List[int]]) -> int:
    surplus = []
    holes = []
    for r in range(3):
        for c in range(3):
            v = grid[r][c]
            if v > 1:
                surplus.extend([(r, c)] * (v - 1))
            elif v == 0:
                holes.append((r, c))
    best = None
    for perm in permutations(surplus):
        total = 0
        for (sr, sc), (hr, hc) in zip(perm, holes):
            total += abs(sr - hr) + abs(sc - hc)
        if best is None or total < best:
            best = total
    return best if best is not None else 0
