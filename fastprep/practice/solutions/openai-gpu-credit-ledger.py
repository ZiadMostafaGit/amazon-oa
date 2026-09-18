# Chronological event replay with a min-heap of active grants ordered by expiry.
from typing import List, Optional, Any
import heapq


def processGpuCredits(operations: List[str]) -> List[str]:
    # (timestamp, phase, input_index, payload); phase: 0 add, 1 subtract, 2 balance
    events = []
    for idx, op in enumerate(operations):
        parts = op.split()
        kind = parts[0].upper()
        if kind == "ADD":
            gid = parts[1]
            amount = int(parts[2])
            start = int(parts[3])
            expire = int(parts[4])
            events.append((start, 0, idx, (gid, amount, expire)))
        elif kind == "SUBTRACT":
            amount = int(parts[1])
            ts = int(parts[2])
            events.append((ts, 1, idx, (amount,)))
        else:  # BALANCE
            ts = int(parts[1])
            events.append((ts, 2, idx, ()))

    events.sort(key=lambda e: (e[0], e[1], e[2]))

    heap = []            # (expire, seq) entries pointing into remaining
    remaining = {}       # seq -> credits left on that grant
    total = 0
    seq = 0
    answers = []

    def expire_through(t):
        nonlocal total
        while heap and heap[0][0] <= t:
            _, key = heapq.heappop(heap)
            total -= remaining.pop(key, 0)

    for ts, phase, idx, payload in events:
        expire_through(ts)
        if phase == 0:
            gid, amount, exp = payload
            if exp > ts and amount > 0:
                remaining[seq] = amount
                total += amount
                heapq.heappush(heap, (exp, seq))
                seq += 1
        elif phase == 1:
            amount = payload[0]
            if amount > total:
                continue
            total -= amount
            need = amount
            while need > 0:
                exp, key = heap[0]
                have = remaining[key]
                if have <= need:
                    need -= have
                    remaining.pop(key)
                    heapq.heappop(heap)
                else:
                    remaining[key] = have - need
                    need = 0
        else:
            answers.append((idx, str(total)))

    answers.sort(key=lambda a: a[0])
    return [v for _, v in answers]
