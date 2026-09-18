# Hash map from message to its last printed timestamp, 10-second window check.
from typing import List, Optional, Any


def shouldPrintMessages(timestamps: List[int], messages: List[str]) -> List[bool]:
    last = {}
    out = []
    for t, m in zip(timestamps, messages):
        prev = last.get(m)
        if prev is None or t - prev >= 10:
            last[m] = t
            out.append(True)
        else:
            out.append(False)
    return out
