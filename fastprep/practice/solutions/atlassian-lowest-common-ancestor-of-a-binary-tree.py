# Iterative traversal building a parent map, then walk p's ancestor chain and climb from q.
from typing import Optional, Any


def lowestCommonAncestorValue(root: Optional[TreeNode], p: int, q: int) -> int:
    if root is None:
        return 0
    parent = {id(root): None}
    node_p = None
    node_q = None
    stack = [root]
    while stack:
        node = stack.pop()
        if node.val == p:
            node_p = node
        if node.val == q:
            node_q = node
        for child in (node.right, node.left):
            if child is not None:
                parent[id(child)] = node
                stack.append(child)
    if node_p is None or node_q is None:
        return root.val

    ancestors = set()
    cur = node_p
    while cur is not None:
        ancestors.add(id(cur))
        cur = parent[id(cur)]
    cur = node_q
    while cur is not None:
        if id(cur) in ancestors:
            return cur.val
        cur = parent[id(cur)]
    return root.val
