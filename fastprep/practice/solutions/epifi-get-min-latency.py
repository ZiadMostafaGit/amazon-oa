# Two-pointer FIFO matching of surplus units to spare capacity along the line (sorted matching minimises the largest hop).
from typing import List, Optional, Any


def getMinLatency(requests: List[int], max_req: List[int]) -> int:
    n = len(requests)
    surplus = []   # (index, units that must leave this server)
    spare = []     # (index, units this server can still absorb)
    total_s = 0
    total_c = 0
    for i in range(n):
        diff = requests[i] - max_req[i]
        if diff > 0:
            surplus.append([i, diff])
            total_s += diff
        elif diff < 0:
            spare.append([i, -diff])
            total_c += -diff
    if total_s > total_c:
        return -1

    best = 0
    j = 0
    for s in surplus:
        si, amount = s
        while amount > 0:
            cj, cap = spare[j]
            if cap == 0:
                j += 1
                continue
            take = amount if amount < cap else cap
            amount -= take
            spare[j][1] -= take
            d = si - cj if si > cj else cj - si
            if d > best:
                best = d
    # the reported latency spans both endpoints of a hop, so a one-step hop counts as 2
    return best + 1 if best > 0 else 0
