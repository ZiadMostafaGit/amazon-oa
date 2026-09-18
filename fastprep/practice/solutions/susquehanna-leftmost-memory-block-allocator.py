# Direct simulation: linear scan for the leftmost run of x free units, with a dict of live allocations.
from typing import List, Optional, Any


def processMemoryQueries(memory: List[int], queries: List[List[int]]) -> List[int]:
    mem = list(memory)
    n = len(mem)
    blocks = {}          # id -> (start, length)
    next_id = 1
    out = []

    for op, arg in queries:
        if op == 0:
            need = arg
            start = -1
            run = 0
            for i in range(n):
                if mem[i] == 0:
                    run += 1
                    if run == need:
                        start = i - need + 1
                        break
                else:
                    run = 0
            if start == -1 or need > n:
                out.append(-1)
            else:
                for i in range(start, start + need):
                    mem[i] = 1
                blocks[next_id] = (start, need)
                next_id += 1
                out.append(start)
        else:
            info = blocks.pop(arg, None)
            if info is None:
                out.append(-1)
            else:
                s, ln = info
                for i in range(s, s + ln):
                    mem[i] = 0
                out.append(ln)
    return out
