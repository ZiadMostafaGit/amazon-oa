# Backtracking over sorted candidates with reuse of the current index; DFS order is lexicographic.
from typing import List, Optional, Any


def combinationSumReuse(candidates: List[int], target: int) -> List[List[int]]:
    vals = sorted(candidates)
    n = len(vals)
    res = []
    path = []

    def dfs(start: int, remaining: int) -> None:
        if remaining == 0:
            res.append(list(path))
            return
        for i in range(start, n):
            v = vals[i]
            if v > remaining:
                break
            path.append(v)
            dfs(i, remaining - v)
            path.pop()

    dfs(0, target)
    return res
