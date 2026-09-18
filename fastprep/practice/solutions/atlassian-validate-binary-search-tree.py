# Iterative in-order traversal: a BST yields strictly increasing values.
from typing import Optional, Any


def isValidBST(root: Optional["TreeNode"]) -> bool:
    stack = []
    node = root
    prev = None
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if prev is not None and node.val <= prev:
            return False
        prev = node.val
        node = node.right
    return True
