# Post-order: compute each subtree's height once, bottom-up, and fail as soon as two children differ by more than one.
from typing import Optional, Any


def isBalanced(root: Optional["TreeNode"]) -> bool:
    if root is None:
        return True
    height = {None: 0}
    stack = [(root, False)]
    while stack:
        node, done = stack.pop()
        if done:
            l, r = height[node.left], height[node.right]
            if abs(l - r) > 1:
                return False
            height[node] = 1 + max(l, r)
        else:
            stack.append((node, True))
            if node.left is not None:
                stack.append((node.left, False))
            if node.right is not None:
                stack.append((node.right, False))
    return True
