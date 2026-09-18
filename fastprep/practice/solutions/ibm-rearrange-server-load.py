# Rearrangement inequality: pair the largest loads with the smallest capacities; break capacity ties by placing the smaller loads at the earlier indices.
from typing import List, Optional, Any


def rearrangeServerLoad(serverCapacity: List[int], serverLoad: List[int]) -> List[int]:
    n = len(serverCapacity)
    order = sorted(range(n), key=lambda i: (serverCapacity[i], i))
    loads = sorted(serverLoad, reverse=True)

    result = [0] * n
    i = 0
    while i < n:
        j = i
        cap = serverCapacity[order[i]]
        while j < n and serverCapacity[order[j]] == cap:
            j += 1
        # positions order[i..j-1] all share this capacity; assign the block
        # of loads loads[i..j-1] to them in ascending order for lexicographic minimality
        block = sorted(loads[i:j])
        for k in range(i, j):
            result[order[k]] = block[k - i]
        i = j
    return result
