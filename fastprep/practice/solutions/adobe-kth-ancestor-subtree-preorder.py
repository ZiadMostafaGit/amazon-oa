from typing import List


def subtreeValuesAfterAncestor(values: List[int], edges: List[List[int]], queries: List[List[int]]) -> List[List[int]]:
    n = len(values)
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:  # edge order fixes each node's child order
        adj[u].append(v)
        adj[v].append(u)
    by_node = [[] for _ in range(n + 1)]
    for qi, (u, k) in enumerate(queries):
        by_node[u].append(qi)
    anc = [0] * len(queries)
    order = []          # preorder values
    tin = [0] * (n + 1)
    size = [1] * (n + 1)
    parent = [0] * (n + 1)
    path = []           # current root-to-node chain
    # Iterative DFS: (node, next adjacency index)
    stack = [[1, 0]]
    parent[1] = 0
    tin[1] = 0
    order.append(values[0])
    path.append(1)
    for qi in by_node[1]:
        k = queries[qi][1]
        anc[qi] = path[-1 - k] if k < len(path) else -1
    while stack:
        top = stack[-1]
        v, i = top
        if i < len(adj[v]):
            top[1] += 1
            c = adj[v][i]
            if c == parent[v]:
                continue
            parent[c] = v
            tin[c] = len(order)
            order.append(values[c - 1])
            path.append(c)
            for qi in by_node[c]:
                k = queries[qi][1]
                anc[qi] = path[-1 - k] if k < len(path) else -1
            stack.append([c, 0])
        else:
            stack.pop()
            path.pop()
            if parent[v]:
                size[parent[v]] += size[v]
    out = []
    for a in anc:
        out.append([-1] if a == -1 else order[tin[a]:tin[a] + size[a]])
    return out
