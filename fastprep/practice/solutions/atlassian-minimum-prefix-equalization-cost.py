# Each prefix operation shifts exactly one adjacent difference, so the answer is the sum of |differences|.
from typing import List, Optional, Any


def findMinimumCost(arr: List[int]) -> int:
    total = 0
    for i in range(1, len(arr)):
        total += abs(arr[i] - arr[i - 1])
    return total
