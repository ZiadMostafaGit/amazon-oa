# Iterative DFS carrying an open (low, high) bound for each node.
from typing import Optional, Any


def isValidBST(root: Optional[TreeNode]) -> bool:
    if root is None:
        return True
    stack = [(root, None, None)]
    while stack:
        node, low, high = stack.pop()
        if low is not None and node.val <= low:
            return False
        if high is not None and node.val >= high:
            return False
        if node.left is not None:
            stack.append((node.left, low, node.val))
        if node.right is not None:
            stack.append((node.right, node.val, high))
    return True
