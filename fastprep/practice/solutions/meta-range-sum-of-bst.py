# DFS that uses the BST ordering to prune: below low only the right side can help, above high only the left.
from typing import Optional, Any


def rangeSumBST(root: Optional["TreeNode"], low: int, high: int) -> int:
    total = 0
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            continue
        if node.val < low:
            stack.append(node.right)
        elif node.val > high:
            stack.append(node.left)
        else:
            total += node.val
            stack.append(node.left)
            stack.append(node.right)
    return total
