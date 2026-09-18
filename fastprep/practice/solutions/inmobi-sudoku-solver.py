# Backtracking with row/column/box bitmasks, filling the most constrained cell first.
from typing import List, Optional, Any


def solveSudoku(board: List[List[str]]) -> List[List[str]]:
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    empties = []
    for r in range(9):
        for c in range(9):
            ch = board[r][c]
            if ch == '.':
                empties.append((r, c))
            else:
                bit = 1 << (int(ch) - 1)
                rows[r] |= bit
                cols[c] |= bit
                boxes[(r // 3) * 3 + c // 3] |= bit

    def solve():
        if not empties:
            return True
        # pick the empty cell with the fewest candidates
        best_i = -1
        best_cnt = 10
        best_mask = 0
        for i, (r, c) in enumerate(empties):
            used = rows[r] | cols[c] | boxes[(r // 3) * 3 + c // 3]
            avail = ~used & 0x1FF
            cnt = bin(avail).count('1')
            if cnt < best_cnt:
                best_cnt = cnt
                best_i = i
                best_mask = avail
                if cnt <= 1:
                    break
        if best_cnt == 0:
            return False
        r, c = empties[best_i]
        b = (r // 3) * 3 + c // 3
        empties[best_i] = empties[-1]
        last = empties.pop()
        mask = best_mask
        while mask:
            bit = mask & -mask
            mask -= bit
            rows[r] |= bit
            cols[c] |= bit
            boxes[b] |= bit
            board[r][c] = str(bit.bit_length())
            if solve():
                return True
            rows[r] ^= bit
            cols[c] ^= bit
            boxes[b] ^= bit
            board[r][c] = '.'
        empties.append(last)
        empties[best_i], empties[-1] = empties[-1], empties[best_i]
        return False

    solve()
    return board
