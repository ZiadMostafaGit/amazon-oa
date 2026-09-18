# Backtracking over sorted values to emit permutations in lexicographic order.
from typing import List, Optional, Any


def permute(nums: List[int]) -> List[List[int]]:
    values = sorted(nums)
    n = len(values)
    used = [False] * n
    current: List[int] = []
    result: List[List[int]] = []

    def backtrack() -> None:
        if len(current) == n:
            result.append(current[:])
            return
        for i in range(n):
            if used[i]:
                continue
            used[i] = True
            current.append(values[i])
            backtrack()
            current.pop()
            used[i] = False

    backtrack()
    return result
