# Sorted free-list heap simulation: best-fit allocation with tail splitting and neighbour coalescing on free.
from typing import List, Optional, Any


def processMallocCommands(heapSize: int, commands: List[str]) -> List[int]:
    free = [[0, heapSize]]  # sorted list of [start, size]
    live = {}               # start offset -> size
    out = []

    for cmd in commands:
        op, arg = cmd.split()
        if op == "ALLOC":
            need = int(arg)
            need = ((need + 7) // 8) * 8
            best = -1
            for i, (start, size) in enumerate(free):
                if size >= need:
                    if best == -1 or size < free[best][1] or (size == free[best][1] and start < free[best][0]):
                        best = i
            if best == -1:
                out.append(-1)
                continue
            start, size = free[best]
            live[start] = need
            if size == need:
                free.pop(best)
            else:
                free[best] = [start + need, size - need]
            out.append(start)
        else:
            offset = int(arg)
            if offset not in live:
                continue
            size = live.pop(offset)
            lo, hi = 0, len(free)
            while lo < hi:
                mid = (lo + hi) // 2
                if free[mid][0] < offset:
                    lo = mid + 1
                else:
                    hi = mid
            free.insert(lo, [offset, size])
            if lo + 1 < len(free) and free[lo][0] + free[lo][1] == free[lo + 1][0]:
                free[lo][1] += free[lo + 1][1]
                free.pop(lo + 1)
            if lo > 0 and free[lo - 1][0] + free[lo - 1][1] == free[lo][0]:
                free[lo - 1][1] += free[lo][1]
                free.pop(lo)

    return out
