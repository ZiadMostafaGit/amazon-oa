# Hierholzer's algorithm (iterative) over lexicographically sorted adjacency lists.
from typing import Dict, List


def findItinerary(tickets: List[List[str]]) -> List[str]:
    adj: Dict[str, List[str]] = {}
    outdeg: Dict[str, int] = {}
    indeg: Dict[str, int] = {}
    for src, dst in tickets:
        adj.setdefault(src, []).append(dst)
        outdeg[src] = outdeg.get(src, 0) + 1
        indeg[dst] = indeg.get(dst, 0) + 1
        outdeg.setdefault(dst, 0)
        indeg.setdefault(src, 0)

    for lst in adj.values():
        lst.sort(reverse=True)  # pop from the end yields the smallest first

    start = None
    for node in sorted(outdeg):
        if outdeg[node] - indeg[node] == 1:
            start = node
            break
    if start is None:
        start = min(adj)

    ptr = {node: len(lst) for node, lst in adj.items()}
    stack = [start]
    route: List[str] = []
    while stack:
        node = stack[-1]
        if ptr.get(node, 0) > 0:
            ptr[node] -= 1
            stack.append(adj[node][ptr[node]])
        else:
            route.append(stack.pop())
    route.reverse()
    return route
