from typing import List, Optional, Any


def canColor(n: int, edges: List[List[int]], m: int) -> bool:
    adj = [set() for _ in range(n)]
    for u, v in edges:
        if u == v:
            return False
        adj[u].add(v)
        adj[v].add(u)
    color = [-1] * n

    def bt(u, used):
        if u == n:
            return True
        # new colors are symmetric: only try one unused color
        for c in range(min(m, used + 1)):
            if all(color[w] != c for w in adj[u]):
                color[u] = c
                if bt(u + 1, max(used, c + 1)):
                    return True
                color[u] = -1
        return False

    return bt(0, 0)
