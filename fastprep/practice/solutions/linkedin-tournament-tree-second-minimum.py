# Approach: iterative DFS with pruning - a subtree whose root exceeds the global min contributes exactly that value.
from typing import Optional


def secondMin(root: Optional['TreeNode']) -> int:
    if root is None:
        return -1
    smallest = root.val
    best = None
    stack = [root]
    while stack:
        node = stack.pop()
        if node.val > smallest:
            if best is None or node.val < best:
                best = node.val
            continue
        if node.left is not None:
            stack.append(node.left)
        if node.right is not None:
            stack.append(node.right)
    return best if best is not None else -1
