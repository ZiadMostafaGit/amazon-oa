# Per-entity sliding window: deques of accepted timestamps per user and per experience, expiring <= t - windowLength.
from collections import deque, defaultdict
from typing import List, Optional, Any


def rateLimiter(requestTimestamps: List[int], userIds: List[int], experienceIds: List[str], windowLength: int, maxRequests: int) -> List[int]:
    user_win = defaultdict(deque)
    exp_win = defaultdict(deque)
    result = []
    for i in range(len(requestTimestamps)):
        t = requestTimestamps[i]
        u = userIds[i]
        e = experienceIds[i]
        cutoff = t - windowLength
        du = user_win[u]
        de = exp_win[e]
        while du and du[0] <= cutoff:
            du.popleft()
        while de and de[0] <= cutoff:
            de.popleft()
        if len(du) < maxRequests and len(de) < maxRequests:
            du.append(t)
            de.append(t)
            result.append(1)
        else:
            result.append(0)
    return result
