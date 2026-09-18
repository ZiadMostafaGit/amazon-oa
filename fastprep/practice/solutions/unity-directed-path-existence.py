# BFS over a hash-map adjacency list of the directed graph.
from collections import deque
from typing import List, Optional, Any


def pathExists(fromNodes: List[int], toNodes: List[int], start: int, target: int) -> bool:
    if start == target:
        return True
    adj = {}
    for i in range(len(fromNodes)):
        u = fromNodes[i]
        v = toNodes[i]
        if u in adj:
            adj[u].append(v)
        else:
            adj[u] = [v]

    seen = {start}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nxt in adj.get(node, ()):
            if nxt == target:
                return True
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return False
