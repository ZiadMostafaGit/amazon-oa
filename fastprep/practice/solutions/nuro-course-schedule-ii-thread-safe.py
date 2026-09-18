# Kahn topological sort with a min-heap per query, over a dedup-ed edge set.
import heapq
from typing import List, Optional, Any


def courseOrderHistory(numCourses: int, operations: List[List[str]]) -> List[str]:
    adj = [set() for _ in range(numCourses)]
    edges = set()
    out = []

    for op in operations:
        if op[0] == "ADD_PREREQUISITE":
            course, prereq = int(op[1]), int(op[2])
            key = (prereq, course)
            if key not in edges:
                edges.add(key)
                adj[prereq].add(course)
            out.append("null")
        else:
            indeg = [0] * numCourses
            for u, v in edges:
                indeg[v] += 1
            heap = [i for i in range(numCourses) if indeg[i] == 0]
            heapq.heapify(heap)
            order = []
            while heap:
                u = heapq.heappop(heap)
                order.append(u)
                for v in adj[u]:
                    indeg[v] -= 1
                    if indeg[v] == 0:
                        heapq.heappush(heap, v)
            if len(order) != numCourses:
                out.append("[]")
            else:
                out.append("[" + ",".join(str(x) for x in order) + "]")
    return out
