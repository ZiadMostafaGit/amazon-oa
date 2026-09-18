# Per-user deque of accepted timestamps; evict those <= t-60, accept while size < 100.
from typing import List, Optional, Any
from collections import defaultdict, deque


def applySlidingWindowRateLimit(userIds: List[str], timestamps: List[int]) -> List[bool]:
    windows = defaultdict(deque)
    out = []
    for uid, t in zip(userIds, timestamps):
        dq = windows[uid]
        while dq and dq[0] <= t - 60:
            dq.popleft()
        if len(dq) < 100:
            dq.append(t)
            out.append(True)
        else:
            out.append(False)
    return out
