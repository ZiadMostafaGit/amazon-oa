# Sliding-window queue: keep hit timestamps in a deque, evict those older than 300s.
from typing import List, Optional, Any
from collections import deque


def runHitCounter(operations: List[str], timestamps: List[int]) -> List[str]:
    hits = deque()
    out = []
    for op, ts in zip(operations, timestamps):
        if op == "hit":
            hits.append(ts)
            out.append("null")
        else:
            while hits and hits[0] < ts - 299:
                hits.popleft()
            out.append(str(len(hits)))
    return out
