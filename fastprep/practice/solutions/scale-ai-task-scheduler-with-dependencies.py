# Lazy min-heap keyed by (deadline, taskId) plus dependency counters; stale entries skipped on pop.
import heapq
from typing import List, Optional, Any


def processOperations(operations: List[List[str]]) -> List[str]:
    deadline = {}          # taskId -> current deadline (added tasks only)
    remaining = {}         # taskId -> number of subtasks not yet consumed
    dependents = {}        # subtaskId -> list of parents waiting on it
    consumed = set()
    heap = []
    out = []

    def make_available(tid):
        heapq.heappush(heap, (deadline[tid], tid))

    for op in operations:
        kind = op[0]
        if kind == "ADD":
            tid = op[1]
            deadline[tid] = int(op[2])
            subs = set(op[3:])
            subs.discard(tid)
            pending = 0
            for s in subs:
                if s not in consumed:
                    pending += 1
                    dependents.setdefault(s, []).append(tid)
            remaining[tid] = pending
            if pending == 0:
                make_available(tid)
        elif kind == "UPDATE":
            tid = op[1]
            if tid in deadline and tid not in consumed:
                deadline[tid] = int(op[2])
                if remaining.get(tid, 0) == 0:
                    make_available(tid)
        else:  # CONSUME
            picked = None
            while heap:
                dl, tid = heapq.heappop(heap)
                if tid in consumed or dl != deadline.get(tid) or remaining.get(tid, 0) != 0:
                    continue
                picked = tid
                break
            if picked is None:
                out.append("NONE")
            else:
                consumed.add(picked)
                out.append(picked)
                for parent in dependents.pop(picked, ()):
                    remaining[parent] -= 1
                    if remaining[parent] == 0 and parent not in consumed:
                        make_available(parent)
    return out
