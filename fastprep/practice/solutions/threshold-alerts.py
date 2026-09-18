# Sliding-window sum over the trailing minutes; alert when the window sum exceeds threshold * window size.
from typing import List, Optional, Any


def numberOfAlerts(precedingMinutes: int, alertThreshold: int, numCalls: List[int]) -> int:
    n = len(numCalls)
    if precedingMinutes > n:
        return 0
    limit = alertThreshold * precedingMinutes
    window = sum(numCalls[:precedingMinutes])
    alerts = 1 if window > limit else 0
    for i in range(precedingMinutes, n):
        window += numCalls[i] - numCalls[i - precedingMinutes]
        if window > limit:
            alerts += 1
    return alerts
