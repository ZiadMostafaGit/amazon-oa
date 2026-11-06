from typing import List, Optional, Any


def isValidDfsOrder(n: int, edges: List[List[int]], order: List[int]) -> bool:
    if len(order) != n or n == 0 or order[0] != 0:
        return False
    if any(not (0 <= x < n) for x in order) or len(set(order)) != n:
        return False
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    rem = [len(adj[v]) for v in range(n)]  # unvisited neighbours left
    visited = [False] * n

    def visit(x):
        visited[x] = True
        for y in adj[x]:
            rem[y] -= 1

    visit(0)
    stack = [0]
    for x in order[1:]:
        while stack and rem[stack[-1]] == 0:
            stack.pop()
        if not stack or x not in adj[stack[-1]]:
            return False
        visit(x)
        stack.append(x)
    return True
