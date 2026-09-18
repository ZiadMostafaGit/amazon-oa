# Append-only position list with per-value queues of live positions and tombstones for O(n + q) removals.
from typing import List, Optional, Any
from collections import deque, defaultdict


def processQueriesOnCart(items: List[int], query: List[int]) -> List[int]:
    values = list(items)
    alive = bytearray([1]) * len(values)
    positions = defaultdict(deque)
    for i, v in enumerate(values):
        positions[v].append(i)
    for q in query:
        if q > 0:
            values.append(q)
            alive.append(1)
            positions[q].append(len(values) - 1)
        else:
            v = -q
            dq = positions.get(v)
            if dq:
                idx = dq.popleft()
                alive[idx] = 0
    return [values[i] for i in range(len(values)) if alive[i]]
