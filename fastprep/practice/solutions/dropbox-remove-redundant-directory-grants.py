# Memoized upward walk: a grant is redundant iff some strict ancestor is granted.
from typing import List, Optional, Any


def removeRedundantGrants(directories: List[str], parents: List[str], grants: List[str]) -> List[str]:
    parent = {}
    for i, d in enumerate(directories):
        p = parents[i] if i < len(parents) else ""
        parent[d] = p if p else None

    granted = set(grants)
    # memo[node] = True if node itself is granted or has a granted ancestor
    memo = {}

    def covered(node):
        # node may be None (above a root)
        stack = []
        cur = node
        while cur is not None and cur not in memo:
            stack.append(cur)
            cur = parent.get(cur)
        val = False if cur is None else memo[cur]
        while stack:
            nd = stack.pop()
            val = val or (nd in granted)
            memo[nd] = val
        return val

    out = []
    for g in grants:
        if not covered(parent.get(g)):
            out.append(g)
    return out
