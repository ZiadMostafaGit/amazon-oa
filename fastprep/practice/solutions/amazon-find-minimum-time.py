# Split apples by side of the origin, then try every split of k between the two sides (nearest first).
from typing import List, Optional, Any


def findMinimumTimeForSnake(n: int, k: int, position: List[int]) -> int:
    left = sorted(-p for p in position if p < 0)
    right = sorted(p for p in position if p > 0)
    free = sum(1 for p in position if p == 0)

    k -= free
    if k <= 0:
        return 0

    best = None
    for i in range(0, k + 1):
        j = k - i
        if i > len(left) or j > len(right):
            continue
        L = left[i - 1] if i > 0 else 0
        R = right[j - 1] if j > 0 else 0
        if i == 0:
            cost = R
        elif j == 0:
            cost = L
        else:
            cost = min(2 * L + R, L + 2 * R)
        if best is None or cost < best:
            best = cost
    return best if best is not None else 0
