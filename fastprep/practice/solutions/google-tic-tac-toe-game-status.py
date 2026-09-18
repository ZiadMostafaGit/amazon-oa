# Simulate moves, checking only the four lines through the newly placed cell for a run of 3.
from typing import List, Optional, Any


def getGameStatus(k: int, n: int, moves: List[List[int]]) -> List[str]:
    board = [[0] * n for _ in range(n)]
    filled = 0
    over = False
    result = []
    dirs = ((0, 1), (1, 0), (1, 1), (1, -1))

    for player, r, c in moves:
        if over:
            result.append("Game Over")
            continue
        if board[r][c] != 0:
            result.append("Invalid Move")
            continue
        board[r][c] = player
        filled += 1

        won = False
        for dr, dc in dirs:
            count = 1
            for sign in (1, -1):
                rr, cc = r + dr * sign, c + dc * sign
                while 0 <= rr < n and 0 <= cc < n and board[rr][cc] == player:
                    count += 1
                    rr += dr * sign
                    cc += dc * sign
            if count >= 3:
                won = True
                break

        if won:
            over = True
            result.append("Player " + str(player) + " won")
        elif filled == n * n:
            over = True
            result.append("Draw")
        else:
            result.append("In Progress")
    return result
