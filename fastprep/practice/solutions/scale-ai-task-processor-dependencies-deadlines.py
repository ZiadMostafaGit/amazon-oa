# Kahn topological sort with a min-heap keyed by (deadline, id).
import heapq
from typing import List, Optional, Any


def consumeTasks(taskIds: List[str], deadlines: List[int], subtasks: List[List[str]]) -> List[str]:
    deadline = {}
    indeg = {}
    dependents = {}
    for i, tid in enumerate(taskIds):
        deadline[tid] = deadlines[i]
        indeg[tid] = 0
        dependents.setdefault(tid, [])
    for i, tid in enumerate(taskIds):
        for sub in subtasks[i]:
            dependents.setdefault(sub, []).append(tid)
            indeg[tid] += 1

    heap = [(deadline[t], t) for t in taskIds if indeg[t] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        _, t = heapq.heappop(heap)
        order.append(t)
        for nxt in dependents.get(t, []):
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, (deadline[nxt], nxt))
    return order
