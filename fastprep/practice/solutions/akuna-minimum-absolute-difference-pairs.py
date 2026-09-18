# Sort, scan adjacent pairs to find the minimum gap, then collect pairs with that gap.
from typing import List


def minimumAbsoluteDifferencePairs(latencies: List[int]) -> List[List[int]]:
    vals = sorted(latencies)
    best = min(vals[i + 1] - vals[i] for i in range(len(vals) - 1))
    return [[vals[i], vals[i + 1]] for i in range(len(vals) - 1)
            if vals[i + 1] - vals[i] == best]
