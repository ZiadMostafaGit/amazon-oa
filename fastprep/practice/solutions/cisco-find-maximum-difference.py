# Approach: single pass tracking the minimum seen so far and the best later-minus-earlier gap.
from typing import List, Optional, Any


def findMaximumDifference(n: int, inputArray: List[int]) -> int:
    if not inputArray:
        return 0
    best = 0
    lowest = inputArray[0]
    for value in inputArray[1:]:
        if value - lowest > best:
            best = value - lowest
        if value < lowest:
            lowest = value
    return best
