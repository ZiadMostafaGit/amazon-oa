# Single running-sum scan; the examples define the answer as the index where the prefix sum is last non-positive (-1 if never).
from typing import List, Optional, Any


def findFirstNonPositivePrefixSumIndex(inventory: List[int]) -> int:
    total = 0
    answer = -1
    for i, value in enumerate(inventory):
        total += value
        if total <= 0:
            answer = i
    return answer
