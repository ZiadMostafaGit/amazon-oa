# Tree DP with an explicit post-order stack: per node keep (best with node taken, best without it).
from typing import Optional, Any


def maxNonAdjacentSum(root: Optional["TreeNode"]) -> int:
    if root is None:
        return 0
    order = []
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        if node.left is not None:
            stack.append(node.left)
        if node.right is not None:
            stack.append(node.right)

    incl = {}
    excl = {}
    for node in reversed(order):
        take = node.val
        skip = 0
        for child in (node.left, node.right):
            if child is None:
                continue
            key = id(child)
            take += excl[key]
            skip += max(incl[key], excl[key])
        key = id(node)
        incl[key] = take
        excl[key] = skip
    return max(incl[id(root)], excl[id(root)])
