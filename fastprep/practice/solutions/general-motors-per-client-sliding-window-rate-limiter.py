# Per-client deque of accepted timestamps; expire entries <= t - window, then compare against the cap.
from collections import deque
from typing import List, Optional, Any


def allowRequests(clientIds: List[str], timestamps: List[int], maxRequests: int, windowSeconds: int) -> List[bool]:
    windows = {}
    out = []
    for cid, t in zip(clientIds, timestamps):
        dq = windows.get(cid)
        if dq is None:
            dq = deque()
            windows[cid] = dq
        cutoff = t - windowSeconds
        while dq and dq[0] <= cutoff:
            dq.popleft()
        if len(dq) < maxRequests:
            dq.append(t)
            out.append(True)
        else:
            out.append(False)
    return out
