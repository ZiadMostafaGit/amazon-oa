# Kahn's topological sort with a min-heap for the lexicographically smallest order.
import heapq
from typing import List, Optional, Any


def solve(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    adj = [[] for _ in range(numCourses)]
    indeg = [0] * numCourses
    for pair in prerequisites:
        course, pre = pair[0], pair[1]
        adj[pre].append(course)
        indeg[course] += 1
    heap = [v for v in range(numCourses) if indeg[v] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        v = heapq.heappop(heap)
        order.append(v)
        for w in adj[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                heapq.heappush(heap, w)
    return order if len(order) == numCourses else []
