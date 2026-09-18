# Hash map of token -> expiry plus a lazy-deletion min-heap so each count is amortized O(log n).
import heapq
from typing import List


def getUnexpiredTokens(time_to_live: int, queries: List[str]) -> List[int]:
    exp = {}
    heap = []
    out = []

    def purge(now: int) -> None:
        while heap and heap[0][0] <= now:
            e, tok = heapq.heappop(heap)
            if exp.get(tok) == e:
                del exp[tok]

    for q in queries:
        parts = q.split()
        op = parts[0]
        if op == "count":
            now = int(parts[1])
            purge(now)
            out.append(len(exp))
        else:
            tok = parts[1]
            now = int(parts[2])
            purge(now)
            if op == "generate":
                e = now + time_to_live
                exp[tok] = e
                heapq.heappush(heap, (e, tok))
            elif op == "renew":
                if tok in exp:
                    e = now + time_to_live
                    exp[tok] = e
                    heapq.heappush(heap, (e, tok))
    return out
