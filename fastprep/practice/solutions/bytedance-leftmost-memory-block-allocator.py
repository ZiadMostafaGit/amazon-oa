# Direct simulation: linear scan for the leftmost free run, dict of active allocations.
from typing import List, Optional, Any


def processMemoryQueries(memory: List[int], queries: List[List[int]]) -> List[int]:
    mem = list(memory)
    n = len(mem)
    alloc = {}
    next_id = 1
    out = []
    for kind, val in queries:
        if kind == 0:
            x = val
            start = -1
            run = 0
            for i in range(n):
                if mem[i] == 0:
                    run += 1
                    if run == x:
                        start = i - x + 1
                        break
                else:
                    run = 0
            if start == -1:
                out.append(-1)
            else:
                for i in range(start, start + x):
                    mem[i] = 1
                alloc[next_id] = (start, x)
                next_id += 1
                out.append(start)
        else:
            aid = val
            if aid in alloc:
                start, length = alloc.pop(aid)
                for i in range(start, start + length):
                    mem[i] = 0
                out.append(length)
            else:
                out.append(-1)
    return out
