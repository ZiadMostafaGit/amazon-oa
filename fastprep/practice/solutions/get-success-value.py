# Sort descending once, prefix sums, then answer each query in O(1).
from typing import List


def findSuccessValue(num_viewers: List[int], queries: List[int]) -> List[int]:
    ordered = sorted(num_viewers, reverse=True)
    prefix = [0] * (len(ordered) + 1)
    for i, v in enumerate(ordered):
        prefix[i + 1] = prefix[i] + v
    out = []
    for k in queries:
        if k < 0:
            k = 0
        elif k > len(ordered):
            k = len(ordered)
        out.append(prefix[k])
    return out
