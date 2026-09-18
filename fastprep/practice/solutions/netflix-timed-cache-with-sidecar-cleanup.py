# Hash map of key -> (value, expiry) with lazy GET check plus a min-heap sidecar for CLEANUP.
import heapq
from typing import List


def runTimedCache(operations: List[str]) -> List[str]:
    store = {}
    expiry_heap = []
    out: List[str] = []
    for op in operations:
        parts = op.split()
        if not parts:
            continue
        cmd = parts[0].upper()
        if cmd == "SET":
            key, value, ttl, now = parts[1], parts[2], int(parts[3]), int(parts[4])
            exp = now + ttl
            store[key] = (value, exp)
            heapq.heappush(expiry_heap, (exp, key))
        elif cmd == "GET":
            key, now = parts[1], int(parts[2])
            entry = store.get(key)
            if entry is None or entry[1] <= now:
                if entry is not None:
                    del store[key]
                out.append("NULL")
            else:
                out.append(entry[0])
        elif cmd == "CLEANUP":
            now = int(parts[1])
            while expiry_heap and expiry_heap[0][0] <= now:
                exp, key = heapq.heappop(expiry_heap)
                cur = store.get(key)
                if cur is not None and cur[1] == exp:
                    del store[key]
    return out
