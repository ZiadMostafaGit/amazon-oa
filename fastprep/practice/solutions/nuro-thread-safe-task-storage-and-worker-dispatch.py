# Simulation: min-heap of queued tasks keyed by original ADD index, plus worker->task map.
import heapq
from typing import List, Optional, Any


def taskWorkerHistory(operations: List[List[str]]) -> List[str]:
    order = {}          # task -> original ADD index
    queued = []         # heap of (add_index, task)
    in_queue = set()    # tasks currently queued
    running = {}        # worker -> task
    completed = set()   # tasks completed
    out = []
    next_idx = 0

    for op in operations:
        kind = op[0]
        if kind == "ADD":
            task = op[1]
            order[task] = next_idx
            next_idx += 1
            heapq.heappush(queued, (order[task], task))
            in_queue.add(task)
            out.append(task + ":QUEUED")
        elif kind == "DISPATCH":
            worker = op[1]
            task = None
            while queued:
                idx, cand = heapq.heappop(queued)
                if cand in in_queue and order[cand] == idx:
                    task = cand
                    in_queue.discard(cand)
                    break
            if task is None:
                out.append("NONE")
            else:
                running[worker] = task
                out.append(task + ":RUNNING")
        elif kind == "COMPLETE":
            worker, task = op[1], op[2]
            if task not in completed:
                completed.add(task)
                if running.get(worker) == task:
                    del running[worker]
            out.append(task + ":COMPLETED")
        elif kind == "FAIL":
            worker, task = op[1], op[2]
            if running.get(worker) == task:
                del running[worker]
            heapq.heappush(queued, (order[task], task))
            in_queue.add(task)
            out.append(task + ":QUEUED")
        elif kind == "RELEASE":
            worker = op[1]
            task = running.pop(worker, None)
            if task is None:
                out.append("NONE")
            else:
                heapq.heappush(queued, (order[task], task))
                in_queue.add(task)
                out.append(task + ":QUEUED")
    return out
