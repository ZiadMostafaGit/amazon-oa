# Group by bid (desc). A group either fits entirely, or round 1 of the round-robin
# (by timestamp) already decides who gets at least one item. O(n log n).
from typing import List, Optional, Any


def getUnfulfilledCustomers(requests: List[List[int]], totalInventory: int) -> List[int]:
    order = sorted(range(len(requests)), key=lambda i: (-requests[i][2], requests[i][3], i))
    got = [False] * len(requests)
    left = totalInventory
    i = 0
    while i < len(order) and left > 0:
        j = i
        bid = requests[order[i]][2]
        while j < len(order) and requests[order[j]][2] == bid:
            j += 1
        group = [t for t in order[i:j] if requests[t][1] > 0]
        for t in group[:left]:
            got[t] = True
        left -= min(left, sum(requests[t][1] for t in group))
        i = j
    return [requests[t][0] for t in range(len(requests)) if not got[t]]
