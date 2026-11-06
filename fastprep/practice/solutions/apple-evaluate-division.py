from typing import List, Optional, Any


def calcEquation(equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
    # weighted union-find: weight[x] = x / parent[x]
    parent = {}
    weight = {}

    def find(x):
        if parent[x] == x:
            return x
        root = find(parent[x])
        weight[x] *= weight[parent[x]]
        parent[x] = root
        return root

    for (a, b), val in zip(equations, values):
        for v in (a, b):
            if v not in parent:
                parent[v] = v
                weight[v] = 1.0
        ra, rb = find(a), find(b)
        if ra != rb:
            # a = wa * ra, b = wb * rb, a / b = val  =>  ra / rb = val * wb / wa
            parent[ra] = rb
            weight[ra] = val * weight[b] / weight[a]

    out = []
    for c, d in queries:
        if c not in parent or d not in parent:
            out.append(-1.0)
            continue
        rc, rd = find(c), find(d)
        out.append(weight[c] / weight[d] if rc == rd else -1.0)
    return out
