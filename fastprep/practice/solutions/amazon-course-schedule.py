# Approach: Kahn's topological sort; all courses processed means no cycle.
from typing import List, Optional, Any
from collections import deque


def solve(numCourses: int, prerequisites: List[List[int]]) -> bool:
    adj = [[] for _ in range(numCourses)]
    indeg = [0] * numCourses
    for pair in prerequisites:
        course, prereq = pair[0], pair[1]
        adj[prereq].append(course)
        indeg[course] += 1
    queue = deque(c for c in range(numCourses) if indeg[c] == 0)
    seen = 0
    while queue:
        node = queue.popleft()
        seen += 1
        for nxt in adj[node]:
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                queue.append(nxt)
    return seen == numCourses
