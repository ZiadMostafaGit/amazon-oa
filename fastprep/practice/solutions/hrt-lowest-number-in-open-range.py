# Single linear scan keeping the minimum value strictly inside the open range.
from typing import List


def findLowestInRange(numbers: List[int], nRange: List[int]) -> int:
    low, high = nRange[0], nRange[1]
    best = None
    for value in numbers:
        if low < value < high and (best is None or value < best):
            best = value
    return 0 if best is None else best
