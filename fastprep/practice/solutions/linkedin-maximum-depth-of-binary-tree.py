# Iterative DFS with an explicit stack to avoid recursion limits on deep trees.
from typing import Optional, Any


def maximumDepth(root: Optional["TreeNode"]) -> int:
    if root is None:
        return 0
    best = 0
    stack = [(root, 1)]
    while stack:
        node, d = stack.pop()
        if d > best:
            best = d
        if node.left is not None:
            stack.append((node.left, d + 1))
        if node.right is not None:
            stack.append((node.right, d + 1))
    return best
