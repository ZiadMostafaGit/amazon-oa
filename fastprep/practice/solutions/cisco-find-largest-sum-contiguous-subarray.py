# Kadane's algorithm: running best-ending-here maximum.
from typing import List, Optional, Any


def findLargestSumContiguousSubarray(inputArr: List[int]) -> int:
    if not inputArr:
        return 0
    best = inputArr[0]
    current = inputArr[0]
    for value in inputArr[1:]:
        current = value if current < 0 else current + value
        if current > best:
            best = current
    return best
