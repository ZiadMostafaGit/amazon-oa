# Bucket accepted timestamps per message into width-10 buckets; each bucket holds <=10 accepted values.
from typing import List, Optional, Any


def shouldPrintOutOfOrder(timestamps: List[int], messages: List[str]) -> List[bool]:
    buckets = {}
    out = []
    for t, m in zip(timestamps, messages):
        b = t // 10
        lo = t - 9
        blocked = False
        for key in ((m, b), (m, b - 1)):
            vals = buckets.get(key)
            if vals:
                for v in vals:
                    if lo <= v <= t:
                        blocked = True
                        break
            if blocked:
                break
        if blocked:
            out.append(False)
        else:
            out.append(True)
            key = (m, b)
            if key in buckets:
                buckets[key].append(t)
            else:
                buckets[key] = [t]
    return out
