# Lazy max-heap of duplicated priorities plus per-priority min-heaps of indices.
import heapq
from typing import List, Optional, Any


def getPrioritiesAfterExecution(priority: List[int]) -> List[int]:
    n = len(priority)
    cur = list(priority)
    alive = [True] * n

    buckets = {}      # priority -> min-heap of candidate indices
    counts = {}       # priority -> number of live processes at that priority
    for i, p in enumerate(priority):
        buckets.setdefault(p, []).append(i)
        counts[p] = counts.get(p, 0) + 1
    for h in buckets.values():
        heapq.heapify(h)

    dup = []          # max-heap (negated) of priorities that may have count >= 2
    for p, c in counts.items():
        if p > 0 and c >= 2:
            heapq.heappush(dup, -p)
    in_dup = {-x for x in dup}

    def mark(p):
        if p > 0 and counts.get(p, 0) >= 2 and p not in in_dup:
            in_dup.add(p)
            heapq.heappush(dup, -p)

    def pop_index(p):
        h = buckets[p]
        while h:
            i = heapq.heappop(h)
            if alive[i] and cur[i] == p:
                return i
        return None

    while dup:
        p = -dup[0]
        if counts.get(p, 0) < 2:
            heapq.heappop(dup)
            in_dup.discard(p)
            continue
        i1 = pop_index(p)
        i2 = pop_index(p)
        if i1 is None or i2 is None:
            # stale bucket contents; resync
            heapq.heappop(dup)
            in_dup.discard(p)
            if i1 is not None:
                heapq.heappush(buckets[p], i1)
            continue

        # execute i1
        alive[i1] = False
        counts[p] -= 1
        # demote i2
        counts[p] -= 1
        np = p // 2
        cur[i2] = np
        buckets.setdefault(np, [])
        heapq.heappush(buckets[np], i2)
        counts[np] = counts.get(np, 0) + 1

        if counts[p] < 2:
            heapq.heappop(dup)
            in_dup.discard(p)
        mark(np)

    return [cur[i] for i in range(n) if alive[i]]
