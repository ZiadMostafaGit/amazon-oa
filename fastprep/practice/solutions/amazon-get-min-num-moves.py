# Positional greedy: bubble the minimum to the front and the maximum to the back, adjusting for crossing.
from typing import List, Optional, Any


def getMinNumMoves(blocks: List[int]) -> int:
    n = len(blocks)
    mn_i = 0
    mx_i = 0
    for i in range(1, n):
        if blocks[i] < blocks[mn_i]:
            mn_i = i
        if blocks[i] > blocks[mx_i]:
            mx_i = i
    moves = mn_i + (n - 1 - mx_i)
    if mn_i > mx_i:
        moves -= 1
    return moves
