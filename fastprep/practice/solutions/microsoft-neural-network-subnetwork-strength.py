# Tree DP with rerooting: weight +1/-1 per node, max-weight connected subtree containing each node.
from typing import List, Optional, Any


def getNeuronStrengths(n: int, neuronFrom: List[int], neuronTo: List[int], strongConnectivity: List[int]) -> List[int]:
    w = [1 if s == 1 else -1 for s in strongConnectivity]

    adj_head = [-1] * n
    m = len(neuronFrom)
    nxt = [-1] * (2 * m)
    to = [0] * (2 * m)
    idx = 0
    for i in range(m):
        a = neuronFrom[i] - 1
        b = neuronTo[i] - 1
        to[idx] = b
        nxt[idx] = adj_head[a]
        adj_head[a] = idx
        idx += 1
        to[idx] = a
        nxt[idx] = adj_head[b]
        adj_head[b] = idx
        idx += 1

    # BFS order from node 0
    parent = [-1] * n
    order = []
    visited = [False] * n
    visited[0] = True
    stack = [0]
    while stack:
        v = stack.pop()
        order.append(v)
        e = adj_head[v]
        while e != -1:
            u = to[e]
            if not visited[u]:
                visited[u] = True
                parent[u] = v
                stack.append(u)
            e = nxt[e]

    # f[v]: best connected subtree inside v's subtree that contains v
    f = w[:]
    for v in reversed(order):
        p = parent[v]
        if p != -1 and f[v] > 0:
            f[p] += f[v]

    # rerooting
    ans = [0] * n
    for v in order:
        p = parent[v]
        if p == -1:
            ans[v] = f[v]
        else:
            outside = ans[p] - (f[v] if f[v] > 0 else 0)
            ans[v] = f[v] + (outside if outside > 0 else 0)

    return ans
