# Sort + two-pointer sliding window: keep the longest window where max <= capacity * min.
from typing import List, Optional, Any


def getMinimumBoxes(boxes: List[int], capacity: int) -> int:
    b = sorted(boxes)
    n = len(b)
    best = 0
    left = 0
    for right in range(n):
        while b[right] > capacity * b[left]:
            left += 1
        if right - left + 1 > best:
            best = right - left + 1
    return n - best
