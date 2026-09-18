# Cycle decomposition of the permutation: answer is n minus the number of cycles.
from typing import List, Optional, Any


def minimumSwaps(values: List[int]) -> int:
    n = len(values)
    order = sorted(range(n), key=lambda i: values[i])
    seen = [False] * n
    swaps = 0
    for i in range(n):
        if seen[i] or order[i] == i:
            seen[i] = True
            continue
        size = 0
        j = i
        while not seen[j]:
            seen[j] = True
            j = order[j]
            size += 1
        swaps += size - 1
    return swaps
