# Approach: Kahn topological sort with a min-heap for the lexicographically smallest order;
# courses left over when the queue empties are exactly the ones trapped by a cycle.
import heapq
from typing import List, Optional, Any


def solve(numCourses: int, prerequisites: List[List[int]]) -> List[List[int]]:
    adj = [[] for _ in range(numCourses)]
    indeg = [0] * numCourses
    for pair in prerequisites:
        if len(pair) < 2:
            continue
        course, prereq = pair[0], pair[1]
        if not (0 <= course < numCourses and 0 <= prereq < numCourses):
            continue
        adj[prereq].append(course)
        indeg[course] += 1

    heap = [c for c in range(numCourses) if indeg[c] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        node = heapq.heappop(heap)
        order.append(node)
        for nxt in adj[node]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)

    if len(order) == numCourses:
        return [order, []]
    blocked = [c for c in range(numCourses) if indeg[c] > 0]
    return [[], blocked]
