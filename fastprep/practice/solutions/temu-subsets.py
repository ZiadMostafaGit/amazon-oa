# Combinations of each size k, generated in index-lexicographic order. O(n * 2^n).
from itertools import combinations
from typing import List, Optional, Any


def subsets(nums: List[int]) -> List[List[int]]:
    out = []
    for k in range(len(nums) + 1):
        for combo in combinations(nums, k):
            out.append(list(combo))
    return out
