# Count subsets with sum exactly k: ways[0] = 1 (the empty subset), every other sum starts at 0.
from typing import List


def countSubsetsWithSum(nums: List[int], k: int) -> int:
    ways = [0] * (k + 1)
    ways[0] = 1
    for v in nums:
        for s in range(k, v - 1, -1):     # downward: each position used at most once
            ways[s] += ways[s - v]
    return ways[k]
