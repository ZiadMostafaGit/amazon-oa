# Count perfect matchings: group values into chains v, v+wt, v+2wt and multiply falling factorials along each chain.
from typing import List, Optional, Any
from collections import Counter

MOD = 10 ** 9 + 7


def numberOfWaysToGroupParcels(weight: List[int], wt: int) -> int:
    n = len(weight)
    if n % 2 != 0 or n == 0:
        return 0
    cnt = Counter(weight)
    d = abs(wt)
    ways = 1
    if d == 0:
        # every pair must be two equal weights
        for c in cnt.values():
            if c % 2 != 0:
                return 0
            k = c - 1
            while k > 0:
                ways = (ways * k) % MOD
                k -= 2
        return ways % MOD

    buckets = {}
    for v in cnt:
        buckets.setdefault(v % d, []).append(v)

    for vals in buckets.values():
        vals.sort()
        leftover = 0
        prev = None
        for v in vals:
            if prev is not None and v != prev + d:
                if leftover != 0:
                    return 0
                leftover = 0
            c = cnt[v]
            if leftover > c:
                return 0
            # number of injections from the leftover items into this value's items
            for t in range(leftover):
                ways = (ways * (c - t)) % MOD
            leftover = c - leftover
            prev = v
        if leftover != 0:
            return 0
    return ways % MOD
