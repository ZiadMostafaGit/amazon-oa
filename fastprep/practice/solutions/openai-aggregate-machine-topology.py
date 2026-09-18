# Iterative preorder DFS over the rooted tree with children sorted by id; subtree sizes via reverse preorder accumulation.
from typing import List, Optional, Any


def aggregateMachineTopology(machineIds: List[int], parentIds: List[int]) -> List[List[int]]:
    n = len(machineIds)
    children = {mid: [] for mid in machineIds}
    parent_of = {}
    root = None
    for i in range(n):
        mid = machineIds[i]
        pid = parentIds[i]
        parent_of[mid] = pid
        if pid == -1:
            root = mid
        else:
            children[pid].append(mid)
    for lst in children.values():
        lst.sort()

    order = []
    depth = {root: 0}
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        d = depth[node] + 1
        kids = children[node]
        for k in reversed(kids):
            depth[k] = d
            stack.append(k)

    size = {node: 1 for node in order}
    for node in reversed(order):
        p = parent_of[node]
        if p != -1:
            size[p] += size[node]

    return [[node, parent_of[node], depth[node], size[node]] for node in order]
