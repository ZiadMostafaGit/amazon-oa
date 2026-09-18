# Doubly linked list over pushed values plus lazy min-heap/max-heap for batch removals.
from typing import List, Optional, Any
import heapq


def stackBatchRemoval(operations: List[str]) -> List[str]:
    # node 0 is the sentinel head
    val = [0]
    prv = [0]
    nxt = [0]
    alive = [False]
    tail = 0
    min_heap = []  # (value, idx)
    max_heap = []  # (-value, idx)
    out = []

    def unlink(i):
        nonlocal tail
        if not alive[i]:
            return
        alive[i] = False
        p = prv[i]
        n = nxt[i]
        nxt[p] = n
        if n != -1:
            prv[n] = p
        if tail == i:
            tail = p

    for line in operations:
        sp = line.find(' ')
        if sp == -1:
            cmd = line
            arg = None
        else:
            cmd = line[:sp]
            arg = int(line[sp + 1:])

        if cmd == "push":
            idx = len(val)
            val.append(arg)
            prv.append(tail)
            nxt.append(-1)
            alive.append(True)
            nxt[tail] = idx
            tail = idx
            heapq.heappush(min_heap, (arg, idx))
            heapq.heappush(max_heap, (-arg, idx))
        elif cmd == "pop":
            if tail != 0:
                unlink(tail)
        elif cmd == "remove_lower":
            while min_heap and min_heap[0][0] < arg:
                _, i = heapq.heappop(min_heap)
                unlink(i)
        elif cmd == "remove_upper":
            while max_heap and -max_heap[0][0] > arg:
                _, i = heapq.heappop(max_heap)
                unlink(i)

        out.append("EMPTY" if tail == 0 else str(val[tail]))

    return out
