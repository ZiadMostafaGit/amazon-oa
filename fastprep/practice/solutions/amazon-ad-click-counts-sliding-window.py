# Per-ad deque of click timestamps, popping ones that fell out of the k-minute window.
from collections import deque, defaultdict
from typing import List, Optional, Any


def countRecentAdClicks(operations: List[str], kMinutes: int) -> List[int]:
    window = 60 * kMinutes
    clicks = defaultdict(deque)
    out = []
    for op in operations:
        kind, ad, ts = op.split(" ")
        t = int(ts)
        if kind == "CLICK":
            clicks[ad].append(t)
        else:
            dq = clicks.get(ad)
            if not dq:
                out.append(0)
                continue
            lo = t - window + 1
            while dq and dq[0] < lo:
                dq.popleft()
            out.append(len(dq))
    return out
