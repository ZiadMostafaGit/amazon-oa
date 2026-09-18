# Hash map of each request id's last timestamp; count consecutive same-id pairs within the gap.
from typing import List, Optional, Any


def getRetryCount(gap: int, requestIds: List[str], timestamps: List[int]) -> int:
    last = {}
    count = 0
    for i, rid in enumerate(requestIds):
        t = timestamps[i]
        prev = last.get(rid)
        if prev is not None and t - prev <= gap:
            count += 1
        last[rid] = t
    return count
