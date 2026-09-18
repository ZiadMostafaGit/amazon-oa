# Value->cell lookup plus row/column/diagonal counters updated per call, stopping at the first full line.
from typing import List, Optional, Any


def firstMingo(board: List[List[int]], called: List[int]) -> List[int]:
    n = len(board)
    pos = {}
    for r in range(n):
        row = board[r]
        for c in range(n):
            pos[row[c]] = (r, c)
    rows = [0] * n
    cols = [0] * n
    diag = 0
    marked = set()
    for i, v in enumerate(called):
        cell = pos.get(v)
        if cell is None or cell in marked:
            continue
        marked.add(cell)
        r, c = cell
        rows[r] += 1
        cols[c] += 1
        if r == c:
            diag += 1
        if rows[r] == n or cols[c] == n or diag == n:
            return [1, i + 1]
    return [0, len(called)]
