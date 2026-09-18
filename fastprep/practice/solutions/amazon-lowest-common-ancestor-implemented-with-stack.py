# Iterative stack DFS over the level-order array building a parent map, then walk ancestors upward.
from typing import List, Optional, Any


def lowestCommonAncestor(root: List[str], p: int, q: int) -> int:
    n = len(root)
    # Build children links from the compact level-order encoding where "null"
    # entries have no children slots of their own.
    left = [-1] * n
    right = [-1] * n
    idx = 1
    for i in range(n):
        if root[i] == "null":
            continue
        if idx < n:
            if root[idx] != "null":
                left[i] = idx
            idx += 1
        if idx < n:
            if root[idx] != "null":
                right[i] = idx
            idx += 1

    parent = {0: -1}
    pos = {}
    stack = [0]
    while stack:
        i = stack.pop()
        pos[int(root[i])] = i
        for c in (left[i], right[i]):
            if c != -1:
                parent[c] = i
                stack.append(c)

    ancestors = set()
    cur = pos[p]
    while cur != -1:
        ancestors.add(cur)
        cur = parent[cur]
    cur = pos[q]
    while cur != -1:
        if cur in ancestors:
            return int(root[cur])
        cur = parent[cur]
    return int(root[0])
