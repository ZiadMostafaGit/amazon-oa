# Sort, then a sliding window counting how many earlier values stay within m of each element.
from typing import List, Optional, Any


def getComputationalEquivalents(process: List[int], m: int) -> int:
    arr = sorted(process)
    total = 0
    left = 0
    for right in range(len(arr)):
        while arr[right] - arr[left] > m:
            left += 1
        total += right - left
    return total
