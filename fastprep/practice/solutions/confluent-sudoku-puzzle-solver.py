# Backtracking with bitmask candidate sets per row, column and 3x3 box.
from typing import List, Optional, Any


def solveSudoku(board: List[List[str]]) -> List[List[str]]:
    grid = [list(row) for row in board]
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    empties = []

    for r in range(9):
        for c in range(9):
            ch = grid[r][c]
            if ch == '.':
                empties.append((r, c))
            else:
                bit = 1 << (ord(ch) - ord('0'))
                rows[r] |= bit
                cols[c] |= bit
                boxes[(r // 3) * 3 + c // 3] |= bit

    full = 0
    for d in range(1, 10):
        full |= 1 << d

    def solve(k: int) -> bool:
        if k == len(empties):
            return True
        # pick the empty cell with fewest candidates (MRV heuristic)
        best = k
        best_count = 10
        best_mask = 0
        for i in range(k, len(empties)):
            r, c = empties[i]
            mask = full & ~(rows[r] | cols[c] | boxes[(r // 3) * 3 + c // 3])
            cnt = bin(mask).count('1')
            if cnt < best_count:
                best_count = cnt
                best = i
                best_mask = mask
                if cnt <= 1:
                    break
        if best_count == 0:
            return False
        empties[k], empties[best] = empties[best], empties[k]
        r, c = empties[k]
        b = (r // 3) * 3 + c // 3
        mask = best_mask
        while mask:
            bit = mask & -mask
            mask -= bit
            d = bit.bit_length() - 1
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            grid[r][c] = str(d)
            if solve(k + 1):
                return True
            rows[r] &= ~bit
            cols[c] &= ~bit
            boxes[b] &= ~bit
            grid[r][c] = '.'
        empties[k], empties[best] = empties[best], empties[k]
        return False

    solve(0)
    return grid
