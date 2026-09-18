# Sort both arrays and pair in order; rearrangement makes matched sorted order optimal for L1 cost.
from typing import List


def findMinimumDist(center: List[int], destination: List[int]) -> int:
    a = sorted(center)
    b = sorted(destination)
    return sum(abs(x - y) for x, y in zip(a, b))
