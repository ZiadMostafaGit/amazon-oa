# Approach: precompute adjacency-difference flags on the circle, then sliding-window count of bad pairs.
from typing import List, Optional, Any


def solution(tileColors: List[int], size: int) -> int:
    n = len(tileColors)
    if size <= 1:
        return n
    # diff[i] == 1 when tile i and tile i+1 (circularly) have different colors
    diff = [1 if tileColors[i] != tileColors[(i + 1) % n] else 0 for i in range(n)]
    # a window starting at i covers pairs diff[i..i+size-2]
    w = size - 1
    cur = sum(diff[j % n] for j in range(w))
    count = 1 if cur == w else 0
    for i in range(1, n):
        cur -= diff[(i - 1) % n]
        cur += diff[(i + w - 1) % n]
        if cur == w:
            count += 1
    return count
