# Kahn's topological sort: schedulable iff every course leaves the queue.
from typing import List, Optional, Any
from collections import deque


def canFinish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    graph = [[] for _ in range(numCourses + 1)]
    indegree = [0] * (numCourses + 1)
    for pair in prerequisites:
        course, prereq = pair[0], pair[1]
        graph[prereq].append(course)
        indegree[course] += 1
    queue = deque(c for c in range(1, numCourses + 1) if indegree[c] == 0)
    done = 0
    while queue:
        u = queue.popleft()
        done += 1
        for v in graph[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    return done == numCourses
