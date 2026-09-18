# Pre-order DFS over the sorted candidates with same-depth duplicate skipping.
from typing import List, Optional, Any


def combinationSumSigned(candidates: List[int], target: int) -> List[List[int]]:
    arr = sorted(candidates)
    n = len(arr)
    res = []
    path = []

    def dfs(start: int, total: int) -> None:
        if total == target:
            res.append(path[:])
        for i in range(start, n):
            if i > start and arr[i] == arr[i - 1]:
                continue
            path.append(arr[i])
            dfs(i + 1, total + arr[i])
            path.pop()

    dfs(0, 0)
    return res
