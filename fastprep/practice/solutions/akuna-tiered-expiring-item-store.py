# Simulation with per-level max-heaps plus a global expiry min-heap, both with lazy deletion.
from typing import List, Optional, Any
import heapq


def processTieredStore(levelCapacities: List[int], operations: List[str]) -> List[str]:
    nlev = len(levelCapacities)
    counts = [0] * nlev
    level_heaps = [[] for _ in range(nlev)]   # (-weight, id, token)
    expiry = []                               # (expiresAt, id, token)
    live = {}                                 # id -> token of currently stored item
    token_seq = 0
    out = []

    def purge(now: int) -> None:
        while expiry and expiry[0][0] <= now:
            _, iid, tok = heapq.heappop(expiry)
            if live.get(iid) == tok:
                del live[iid]
                counts[tok_level[tok]] -= 1

    tok_level = {}

    for op in operations:
        parts = op.split()
        if parts[0] == "STORE":
            iid = parts[1]
            weight = int(parts[2])
            exp = int(parts[3])
            if iid in live:
                out.append("false")
                continue
            placed = -1
            for i in range(nlev):
                if counts[i] < levelCapacities[i]:
                    placed = i
                    break
            if placed < 0:
                out.append("false")
                continue
            token_seq += 1
            tok = token_seq
            live[iid] = tok
            tok_level[tok] = placed
            counts[placed] += 1
            heapq.heappush(level_heaps[placed], (-weight, iid, tok))
            heapq.heappush(expiry, (exp, iid, tok))
            out.append("true")
        else:
            now = int(parts[1])
            purge(now)
            chosen = -1
            for i in range(nlev):
                cap = levelCapacities[i]
                if counts[i] > 0 and 2 * (cap - counts[i]) >= cap:
                    chosen = i
                    break
            if chosen < 0:
                out.append("null")
                continue
            h = level_heaps[chosen]
            res = "null"
            while h:
                negw, iid, tok = heapq.heappop(h)
                if live.get(iid) == tok:
                    del live[iid]
                    counts[chosen] -= 1
                    res = iid
                    break
            out.append(res)
    return out
