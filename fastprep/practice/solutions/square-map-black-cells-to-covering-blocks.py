# Direct enumeration: each cell is covered by up to 4 blocks with top-left in {r-1,r} x {c-1,c}, clipped to bounds.
from typing import List


def mapBlackCellsToBlocks(rows: int, cols: int, blackCells: List[List[int]]) -> List[List[int]]:
    out = []
    for r, c in sorted((cell[0], cell[1]) for cell in blackCells):
        rec = [r, c]
        for br in (r - 1, r):
            if br < 0 or br > rows - 2:
                continue
            for bc in (c - 1, c):
                if bc < 0 or bc > cols - 2:
                    continue
                rec.append(br)
                rec.append(bc)
        out.append(rec)
    return out
