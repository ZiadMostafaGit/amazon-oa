# Queue simulation with expiry buckets: each request is removed at most once, O(n + maxWait).
from typing import List, Optional, Any


def findRequestsInQueue(wait: List[int]) -> List[int]:
    n = len(wait)
    if n == 0:
        return [0]

    # buckets[t] = indices of requests that expire when time reaches t
    buckets = {}
    for i, w in enumerate(wait):
        buckets.setdefault(w, []).append(i)

    removed = [False] * n
    alive = n
    front = 0

    res = [alive]
    served = front  # request processed at time 0

    t = 1
    while True:
        # the request processed at t-1 leaves the queue now
        if not removed[served]:
            removed[served] = True
            alive -= 1
        # requests whose waiting time has run out leave too
        for i in buckets.get(t, ()):
            if not removed[i]:
                removed[i] = True
                alive -= 1
        res.append(alive)
        if alive == 0:
            break
        while removed[front]:
            front += 1
        served = front
        t += 1

    return res
