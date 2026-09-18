# Direct simulation of the round-robin allocation with lazy rebuilds of the live-center list.
from typing import List, Optional, Any


def mostPackagesProcessed(centerCapacities: List[int], dailyLog: List[str]) -> int:
    n = len(centerCapacities)
    closed = [False] * n
    counts = [0] * n
    rem = list(centerCapacities)
    live = list(range(n))
    p = 0
    dirty = False

    for entry in dailyLog:
        if entry == "PACKAGE":
            target = -1
            while True:
                while p < len(live):
                    c = live[p]
                    if closed[c] or rem[c] == 0:
                        p += 1
                    else:
                        break
                if p < len(live):
                    target = live[p]
                    break
                # passed the end of the array: one full rotation finished
                if dirty:
                    live = [i for i in live if not closed[i]]
                    dirty = False
                if not live:
                    break
                for i in live:
                    rem[i] = centerCapacities[i]
                p = 0
            if target < 0:
                continue
            rem[target] -= 1
            counts[target] += 1
        else:
            j = int(entry.split()[1])
            if not closed[j]:
                closed[j] = True
                dirty = True

    best = 0
    for i in range(n):
        if counts[i] >= counts[best]:
            best = i
    return best
