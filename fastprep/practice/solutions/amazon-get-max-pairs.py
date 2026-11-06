from typing import List


def getMaxPairs(frontend: List[int], backend: List[int]) -> int:
    f = sorted(frontend)
    b = sorted(backend)
    pairs = 0
    j = 0
    for x in f:  # smallest frontend first: it grabs the smallest backend it beats
        if j < len(b) and x > b[j]:
            pairs += 1
            j += 1
    return pairs
