# Sorted backtracking with duplicate skipping at each recursion depth.
from typing import List, Optional, Any


def combinationSumSingleUse(candidates: List[int], target: int) -> List[List[int]]:
    nums = sorted(candidates)
    n = len(nums)
    res: List[List[int]] = []
    path: List[int] = []

    def dfs(start: int, remain: int) -> None:
        if remain == 0:
            res.append(path[:])
            return
        i = start
        while i < n:
            v = nums[i]
            if v > remain:
                break
            if i > start and nums[i] == nums[i - 1]:
                i += 1
                continue
            path.append(v)
            dfs(i + 1, remain - v)
            path.pop()
            i += 1

    dfs(0, target)
    return res
