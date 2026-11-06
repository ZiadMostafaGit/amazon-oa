# Knapsack with two dimensions: how many positions are taken, and which sums they reach.
from typing import List


def hasKSubsetSum(nums: List[int], k: int, target: int) -> bool:
    reach = [set() for _ in range(k + 1)]   # reach[j] = sums of some j chosen positions
    reach[0].add(0)
    for v in nums:
        for j in range(k, 0, -1):            # downward in count: each position used once
            if reach[j - 1]:
                reach[j] |= {s + v for s in reach[j - 1]}
    return target in reach[k]
