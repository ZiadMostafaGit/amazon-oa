# Weighted completion-time scheduling (Smith's rule): sort servers by kill-time / request-rate.
from typing import List
from functools import cmp_to_key


def minimumRequests(request: List[int], health: List[int], k: int) -> int:
    n = len(request)
    jobs = []
    for i in range(n):
        t = -(-health[i] // k)  # seconds of virus needed to bring server i down
        jobs.append((t, request[i]))

    # Minimize sum(w_i * C_i): order by t/w ascending, compared without floats.
    def cmp(a, b):
        left = a[0] * b[1]
        right = b[0] * a[1]
        if left < right:
            return -1
        if left > right:
            return 1
        return 0

    jobs.sort(key=cmp_to_key(cmp))

    total = 0
    elapsed = 0
    for t, w in jobs:
        elapsed += t
        total += w * elapsed
    return total + 1
