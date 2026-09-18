# Iterative in-order traversal with an explicit stack, stopping at the kth visited node.
from typing import Optional, Any


def kthSmallest(root: Optional["TreeNode"], k: int) -> int:
    stack = []
    node = root
    while node or stack:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.right
    return -1
