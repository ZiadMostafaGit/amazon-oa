# Row-by-row backtracking: place one queen per row, pruning columns and both diagonals already attacked.
from typing import List, Optional, Any


def solveNQueens(n: int) -> List[List[str]]:
    out = []
    cols = [0] * n
    used_col, used_d1, used_d2 = set(), set(), set()

    def place(r):
        if r == n:
            out.append(["." * c + "Q" + "." * (n - c - 1) for c in cols])
            return
        for c in range(n):
            if c in used_col or (r - c) in used_d1 or (r + c) in used_d2:
                continue
            cols[r] = c
            used_col.add(c); used_d1.add(r - c); used_d2.add(r + c)
            place(r + 1)
            used_col.discard(c); used_d1.discard(r - c); used_d2.discard(r + c)

    place(0)
    return out
