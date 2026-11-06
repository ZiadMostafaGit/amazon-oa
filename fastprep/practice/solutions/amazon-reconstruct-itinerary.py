# Hierholzer's algorithm for an Eulerian path, taking smallest destinations first. O(E log E).
from collections import defaultdict
from typing import List, Optional, Any


def findItinerary(tickets: List[List[str]]) -> List[str]:
    graph = defaultdict(list)
    for a, b in sorted(tickets, reverse=True):
        graph[a].append(b)
    route, stack = [], ["JFK"]
    while stack:
        while graph[stack[-1]]:
            stack.append(graph[stack[-1]].pop())
        route.append(stack.pop())
    return route[::-1]
