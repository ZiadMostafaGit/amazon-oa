# Sorted backtracking; skip equal values at the same depth to avoid duplicate combinations.
from typing import List, Optional, Any


def combinationSumOnce(candidates: List[int], target: int) -> List[List[int]]:
    nums = sorted(candidates)
    out, path = [], []

    def go(start, remain):
        if remain == 0:
            out.append(path[:])
            return
        for i in range(start, len(nums)):
            if nums[i] > remain:
                break
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            go(i + 1, remain - nums[i])
            path.pop()

    go(0, target)
    return out
