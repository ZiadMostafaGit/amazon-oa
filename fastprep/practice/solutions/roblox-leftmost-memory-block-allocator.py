# Direct simulation: linear scan for the leftmost run of free units, with an id -> (start, length) map.
from typing import List


def processMemoryQueries(memory: List[int], queries: List[List[int]]) -> List[int]:
    mem = list(memory)
    n = len(mem)
    blocks = {}
    next_id = 1
    out = []
    for q in queries:
        kind, arg = q[0], q[1]
        if kind == 0:
            size = arg
            start = -1
            if size <= 0:
                start = 0
            else:
                run = 0
                for i in range(n):
                    if mem[i] == 0:
                        run += 1
                        if run == size:
                            start = i - size + 1
                            break
                    else:
                        run = 0
            if start == -1:
                out.append(-1)
            else:
                for i in range(start, start + size):
                    mem[i] = 1
                blocks[next_id] = (start, size)
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
