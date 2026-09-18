# Sliding window over a deque of hit timestamps, evicting anything older than t-299 on each query.
from typing import List, Optional, Any
from collections import deque


def countRecentHits(operationTypes: List[int], timestamps: List[int]) -> List[int]:
    hits = deque()
    results = []
    for op, t in zip(operationTypes, timestamps):
        if op == 0:
            hits.append(t)
        else:
            cutoff = t - 299
            while hits and hits[0] < cutoff:
                hits.popleft()
            results.append(len(hits))
    return results
