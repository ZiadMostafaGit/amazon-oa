from typing import List, Optional, Any


def minimumTreeValue(n: int, k: int, values: List[int], edges: List[List[int]]) -> int:
    # Final total = sum(value * depth), root depth 1. A moved node ends best as a
    # child of the root (depth 2). A node can be moved only after its whole
    # subtree is moved, so the moved set is a union of disjoint full subtrees.
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    depth = [0] * (n + 1)
    parent = [0] * (n + 1)
    order = []
    depth[1] = 1
    stack = [1]
    seen = [False] * (n + 1)
    seen[1] = True
    while stack:
        u = stack.pop()
        order.append(u)
        for w in adj[u]:
            if not seen[w]:
                seen[w] = True
                parent[w] = u
                depth[w] = depth[u] + 1
                stack.append(w)
    total = sum(values[v - 1] * depth[v] for v in range(1, n + 1))
    size = [1] * (n + 1)
    gain = [0] * (n + 1)  # gain of moving the whole subtree
    dp = [None] * (n + 1)
    for u in reversed(order):
        cur = [0]
        g = values[u - 1] * (depth[u] - 2) if u != 1 else 0
        for w in adj[u]:
            if w == parent[u] and u != 1:
                continue
            if parent[w] != u:
                continue
            size[u] += size[w]
            g += gain[w]
            cw = dp[w]
            lim = min(k, len(cur) - 1 + len(cw) - 1)
            new = cur + [-1] * (lim + 1 - len(cur))
            for a in range(len(cur)):
                ca = cur[a]
                if ca < 0:
                    continue
                for b in range(1, min(len(cw), lim - a + 1)):
                    if cw[b] >= 0 and ca + cw[b] > new[a + b]:
                        new[a + b] = ca + cw[b]
            cur = new
            dp[w] = None
        gain[u] = g
        if u != 1 and size[u] <= k:
            if len(cur) <= size[u]:
                cur = cur + [-1] * (size[u] + 1 - len(cur))
            if g > cur[size[u]]:
                cur[size[u]] = g
        dp[u] = cur
    return total - max(dp[1][: k + 1])
