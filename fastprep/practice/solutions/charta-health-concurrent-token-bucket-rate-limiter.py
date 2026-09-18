# Token-bucket simulation with tokens scaled by 1000 so millisecond refills stay exact integers.
from typing import List, Optional, Any


def applyTokenBucket(capacity: int, refillPerSecond: int, timestamps: List[int], requestedTokens: List[int]) -> List[bool]:
    cap = capacity * 1000
    tokens = cap
    last = 0
    res = []
    for t, need in zip(timestamps, requestedTokens):
        dt = t - last
        if dt > 0:
            tokens = min(cap, tokens + refillPerSecond * dt)
            last = t
        want = need * 1000
        if tokens >= want:
            tokens -= want
            res.append(True)
        else:
            res.append(False)
    return res
