from typing import List, Optional, Any


def hasDirectedCycle(n: int, edges: List[List[int]]) -> bool:
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
    # 0 = unvisited, 1 = on the current DFS path, 2 = finished
    color = [0] * n
    for s in range(n):
        if color[s]:
            continue
        color[s] = 1
        stack = [(s, 0)]
        while stack:
            u, i = stack[-1]
            if i < len(adj[u]):
                stack[-1] = (u, i + 1)
                v = adj[u][i]
                if color[v] == 1:
                    return True
                if color[v] == 0:
                    color[v] = 1
                    stack.append((v, 0))
            else:
                color[u] = 2
                stack.pop()
    return False
