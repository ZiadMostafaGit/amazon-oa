from typing import List, Optional, Any
import heapq


def findOrder(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    adj = [[] for _ in range(numCourses)]
    indeg = [0] * numCourses
    for course, pre in prerequisites:
        adj[pre].append(course)
        indeg[course] += 1
    ready = [c for c in range(numCourses) if indeg[c] == 0]
    heapq.heapify(ready)
    order = []
    while ready:
        u = heapq.heappop(ready)
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                heapq.heappush(ready, v)
    return order if len(order) == numCourses else []
