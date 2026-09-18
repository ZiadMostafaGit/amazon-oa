# Iterative DFS carrying an open (low, high) bound for each node.
from typing import Optional, Any


def validateBST(root: Optional["TreeNode"]) -> bool:
    stack = [(root, None, None)]
    while stack:
        node, low, high = stack.pop()
        if node is None:
            continue
        if low is not None and node.val <= low:
            return False
        if high is not None and node.val >= high:
            return False
        stack.append((node.left, low, node.val))
        stack.append((node.right, node.val, high))
    return True
