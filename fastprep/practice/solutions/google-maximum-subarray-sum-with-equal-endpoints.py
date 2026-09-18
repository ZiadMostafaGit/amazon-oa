# Prefix sums plus a per-value minimum earlier prefix, one pass.
from typing import List, Optional, Any


def maximumEqualEndpointSum(nums: List[int]) -> int:
    best = None
    prefix = 0
    min_prefix = {}
    for v in nums:
        cur = min_prefix.get(v)
        if cur is None or prefix < cur:
            min_prefix[v] = prefix
            cur = prefix
        prefix += v
        cand = prefix - cur
        if best is None or cand > best:
            best = cand
    return best
