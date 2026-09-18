# Simulation with incremental row/col/diagonal counters per player.
from typing import List, Optional, Any


def playTicTacToe(n: int, moves: List[List[int]]) -> List[str]:
    rows = [[0] * n, [0] * n]
    cols = [[0] * n, [0] * n]
    diag = [0, 0]
    anti = [0, 0]
    board = [[0] * n for _ in range(n)]
    turn = 0  # 0 -> X, 1 -> O
    filled = 0
    over = False
    res = []
    for mv in moves:
        if over:
            res.append("GAME_OVER")
            continue
        r, c = mv[0], mv[1]
        if r < 0 or r >= n or c < 0 or c >= n or board[r][c] != 0:
            res.append("INVALID")
            continue
        board[r][c] = turn + 1
        filled += 1
        rows[turn][r] += 1
        cols[turn][c] += 1
        if r == c:
            diag[turn] += 1
        if r + c == n - 1:
            anti[turn] += 1
        won = (rows[turn][r] == n or cols[turn][c] == n
               or (r == c and diag[turn] == n)
               or (r + c == n - 1 and anti[turn] == n))
        if won:
            over = True
            res.append("X_WINS" if turn == 0 else "O_WINS")
        elif filled == n * n:
            over = True
            res.append("DRAW")
        else:
            res.append("CONTINUE")
            turn ^= 1
    return res
