# Precompute the greedy max plantable count once, then answer each query in O(1).
from typing import List, Optional, Any


def flowerbedCapacityQueries(flowerbed: List[int], queries: List[int]) -> List[bool]:
    bed = list(flowerbed)
    n = len(bed)
    capacity = 0
    for i in range(n):
        if bed[i] == 0 and (i == 0 or bed[i - 1] == 0) and (i == n - 1 or bed[i + 1] == 0):
            bed[i] = 1
            capacity += 1
    return [q <= capacity for q in queries]
