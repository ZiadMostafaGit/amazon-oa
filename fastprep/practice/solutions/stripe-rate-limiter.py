# Per-key deque of hit timestamps; evict entries with t0 <= t - windowSeconds (sliding window).
from collections import deque
from typing import List


def runRateLimiter(maxRequests: int, windowSeconds: int, operations: List[str]) -> List[str]:
    hits = {}
    out = []
    for op in operations:
        parts = op.split()
        if not parts:
            continue
        cmd, key, ts = parts[0], parts[1], int(parts[2])
        dq = hits.get(key)
        if dq is None:
            dq = deque()
            hits[key] = dq
        cutoff = ts - windowSeconds
        while dq and dq[0] <= cutoff:
            dq.popleft()
        if cmd == "hit":
            dq.append(ts)
        else:
            out.append("true" if len(dq) < maxRequests else "false")
    return out
