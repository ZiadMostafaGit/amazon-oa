# Track the current strictly increasing run length and count windows of size k that fit inside it.
from typing import List, Optional, Any


def countIncreasingWindows(yCoordinates: List[int], k: int) -> int:
    n = len(yCoordinates)
    if k > n:
        return 0
    if k == 1:
        return n
    total = 0
    run = 1
    for i in range(1, n):
        run = run + 1 if yCoordinates[i - 1] < yCoordinates[i] else 1
        if run >= k:
            total += 1
    return total
