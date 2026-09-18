# Single pass with an insertion-ordered dict keeping the max timestamp (ties -> later event) and a count.
from typing import List, Optional, Any


def summarizeByDevice(events: List[List[str]]) -> List[List[str]]:
    latest = {}
    for ev in events:
        _, device, status, ts = ev[0], ev[1], ev[2], ev[3]
        t = int(ts)
        rec = latest.get(device)
        if rec is None:
            latest[device] = [status, ts, t, 1]
        else:
            rec[3] += 1
            if t >= rec[2]:
                rec[0] = status
                rec[1] = ts
                rec[2] = t
    return [[d, r[0], r[1], str(r[3])] for d, r in latest.items()]
