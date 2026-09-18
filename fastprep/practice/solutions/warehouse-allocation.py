# Approach: the optimal final multiset is sum//n boxes everywhere plus one extra on sum%n piles; give the extras to the largest piles and count surplus moves.
from typing import List, Optional, Any


def findMinimumOperations(boxes: List[int]) -> int:
    n = len(boxes)
    if n == 0:
        return 0
    total = sum(boxes)
    base, extra = divmod(total, n)
    order = sorted(boxes, reverse=True)
    moves = 0
    for i, value in enumerate(order):
        target = base + 1 if i < extra else base
        if value > target:
            moves += value - target
    return moves
