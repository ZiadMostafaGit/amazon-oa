# Backtracking over the increasing digits 1..9 with sum/count pruning.
from typing import List, Optional, Any


def fixedLengthCombinationSum(k: int, target: int) -> List[List[int]]:
    result: List[List[int]] = []
    current: List[int] = []

    def backtrack(start: int, remaining: int) -> None:
        if len(current) == k:
            if remaining == 0:
                result.append(current[:])
            return
        slots = k - len(current)
        for value in range(start, 10):
            if value > remaining:
                break
            # smallest achievable sum with the remaining slots starting at value
            smallest = slots * value + (slots * (slots - 1)) // 2
            if smallest > remaining:
                break
            current.append(value)
            backtrack(value + 1, remaining - value)
            current.pop()

    backtrack(1, target)
    return result
