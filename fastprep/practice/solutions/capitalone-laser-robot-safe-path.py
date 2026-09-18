# Mark laser rows/columns, then walk each of the four directions counting safe cells.
from typing import List, Optional, Any


def laserRobotSafePath(numRows: int, numColumns: int, curRow: int, curColumn: int, laserCoordinates: List[List[int]]) -> int:
    hit_rows = set()
    hit_cols = set()
    for r, c in laserCoordinates or []:
        hit_rows.add(r)
        hit_cols.add(c)

    best = 0
    for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        steps = 0
        r, c = curRow + dr, curColumn + dc
        while 1 <= r <= numRows and 1 <= c <= numColumns:
            if r in hit_rows or c in hit_cols:
                break
            steps += 1
            r += dr
            c += dc
        if steps > best:
            best = steps
    return best
