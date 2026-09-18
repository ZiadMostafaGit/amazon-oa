# Parity check: a valid chessboard has cell (i,j) equal to board[0][0] XOR ((i+j) & 1).
from typing import List


def solve(board: List[List[int]]) -> bool:
    base = board[0][0]
    for i, row in enumerate(board):
        for j, val in enumerate(row):
            if val != (base ^ ((i + j) & 1)):
                return False
    return True
