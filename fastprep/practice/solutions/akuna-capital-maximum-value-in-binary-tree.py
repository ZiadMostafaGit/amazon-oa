# Iterative DFS over the tree tracking the running maximum node value.
from typing import Optional, Any


def findMaximumValue(root: Optional["TreeNode"]) -> int:
    best = None
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            continue
        if best is None or node.val > best:
            best = node.val
        stack.append(node.left)
        stack.append(node.right)
    return best
