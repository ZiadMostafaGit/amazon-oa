# Greedy: base sum of min(capacity, requests), then add the k largest doubling gains.
from typing import List


def maximumHandledRequests(serverCapacity: List[int], incomingRequests: List[int], k: int) -> int:
    total = 0
    gains = []
    for c, r in zip(serverCapacity, incomingRequests):
        base = c if c < r else r
        upgraded = (2 * c) if (2 * c) < r else r
        total += base
        gains.append(upgraded - base)
    gains.sort(reverse=True)
    for i in range(min(k, len(gains))):
        g = gains[i]
        if g <= 0:
            break
        total += g
    return total
