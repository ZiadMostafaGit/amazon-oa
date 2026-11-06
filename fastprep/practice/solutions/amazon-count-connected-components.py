from typing import List, Optional, Any


def countConnectedComponents(n: int, edges: List[List[int]]) -> int:
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * n
    components = 0
    for s in range(n):
        if seen[s]:
            continue
        components += 1
        seen[s] = True
        stack = [s]
        while stack:
            u = stack.pop()
            for v in adj[u]:
                if not seen[v]:
                    seen[v] = True
                    stack.append(v)
    return components
