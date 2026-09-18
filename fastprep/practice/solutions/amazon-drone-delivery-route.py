from typing import List, Optional, Any


def getMinimumDroneTime(transitionTime: List[int], requestedHubs: List[int]) -> int:
    m = len(transitionTime) if transitionTime else 0
    if m == 0 or not requestedHubs:
        return 0

    # pfx[i] = transitionTime[1] + ... + transitionTime[i]   (1-based hubs)
    pfx = [0] * (m + 1)
    for i in range(1, m + 1):
        pfx[i] = pfx[i - 1] + transitionTime[i - 1]
    total = pfx[m]

    def clockwise(a: int, b: int) -> int:
        # leaves hubs a, a+1, ..., b-1, paying the departure hub's time each step
        if b >= a:
            return pfx[b - 1] - pfx[a - 1]
        return total - pfx[a - 1] + pfx[b - 1]

    def counter(a: int, b: int) -> int:
        # leaves hubs a, a-1, ..., b+1
        if b <= a:
            return pfx[a] - pfx[b]
        return total - pfx[b] + pfx[a]

    answer = 0
    cur = 1
    for hub in requestedHubs:
        if hub != cur:
            answer += min(clockwise(cur, hub), counter(cur, hub))
            cur = hub
    return answer
