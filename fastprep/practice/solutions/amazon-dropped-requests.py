# Index-offset sliding windows: request i violates a cap when the i-k-th request is still in range.
from typing import List, Optional, Any


def droppedRequests(requestTime: List[int]) -> int:
    dropped = 0
    n = len(requestTime)
    for i in range(n):
        t = requestTime[i]
        if i >= 3 and requestTime[i - 3] == t:
            dropped += 1
        elif i >= 20 and requestTime[i - 20] >= t - 9:
            dropped += 1
        elif i >= 60 and requestTime[i - 60] >= t - 59:
            dropped += 1
    return dropped
