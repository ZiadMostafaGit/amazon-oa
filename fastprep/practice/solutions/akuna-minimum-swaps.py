# Permutation cycle decomposition against the target descending order: answer = n - number of cycles.
from typing import List


def minimumSwaps(popularity: List[int]) -> int:
    n = len(popularity)
    # target position of the element currently at index i
    order = sorted(range(n), key=lambda i: -popularity[i])
    target = [0] * n
    for pos, idx in enumerate(order):
        target[idx] = pos

    seen = [False] * n
    swaps = 0
    for i in range(n):
        if seen[i]:
            continue
        size = 0
        j = i
        while not seen[j]:
            seen[j] = True
            j = target[j]
            size += 1
        swaps += size - 1
    return swaps
