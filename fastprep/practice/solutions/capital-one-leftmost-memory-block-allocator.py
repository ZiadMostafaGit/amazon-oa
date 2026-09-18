# Direct simulation: linear scan for the leftmost run of x free units, with a map from allocation id to (start, length).
from typing import List, Optional, Any


def processMemoryQueries(memory: List[int], queries: List[List[int]]) -> List[int]:
    n = len(memory)
    mem = list(memory)
    owner = {}          # allocation id -> (start, length)
    next_id = 1
    out = []

    for q in queries:
        op, arg = q[0], q[1]
        if op == 0:
            x = arg
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
                owner[next_id] = (start, x)
                out.append(start)
                next_id += 1
        else:
            aid = arg
            if aid not in owner:
                out.append(-1)
            else:
                s, ln = owner.pop(aid)
                for i in range(s, s + ln):
                    mem[i] = 0
                out.append(ln)

    return out
