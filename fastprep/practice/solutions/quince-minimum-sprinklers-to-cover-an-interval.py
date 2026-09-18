# Greedy jump-game: best reach from each start position, then minimum jumps to cover [0, n].
from typing import List, Optional, Any


def minSprinklers(n: int, ranges: List[int]) -> int:
    far = [0] * (n + 1)
    for i, r in enumerate(ranges):
        left = max(0, i - r)
        right = min(n, i + r)
        if right > far[left]:
            far[left] = right
    count = 0
    end = 0
    farthest = 0
    i = 0
    while end < n:
        while i <= end:
            if far[i] > farthest:
                farthest = far[i]
            i += 1
        if farthest <= end:
            return -1
        end = farthest
        count += 1
    return count
