# Sliding window of size 3: a window is good iff its distinct-value count is exactly 2.
from typing import List, Optional, Any


def solution(a: List[int]) -> int:
    count = 0
    for i in range(len(a) - 2):
        x, y, z = a[i], a[i + 1], a[i + 2]
        if len({x, y, z}) == 2:
            count += 1
    return count
