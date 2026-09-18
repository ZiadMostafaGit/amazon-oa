# Iterative DFS carrying the running sum down to each leaf.
from typing import Optional, Any


def hasPathSum(root: Optional[TreeNode], targetSum: int) -> bool:
    if root is None:
        return False
    stack = [(root, root.val)]
    while stack:
        node, total = stack.pop()
        if node.left is None and node.right is None:
            if total == targetSum:
                return True
            continue
        if node.left is not None:
            stack.append((node.left, total + node.left.val))
        if node.right is not None:
            stack.append((node.right, total + node.right.val))
    return False
