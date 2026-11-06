# Post-order: each node returns its height; the best path through a node is left height + right height.
# Iterative so a 100000-deep chain does not overflow the call stack.
from typing import Optional, Any


def diameterOfBinaryTree(root: Optional["TreeNode"]) -> int:
    if root is None:
        return 0
    height = {None: 0}
    best = 0
    stack = [(root, False)]
    while stack:
        node, done = stack.pop()
        if done:
            l, r = height[node.left], height[node.right]
            best = max(best, l + r)
            height[node] = 1 + max(l, r)
        else:
            stack.append((node, True))
            if node.left is not None:
                stack.append((node.left, False))
            if node.right is not None:
                stack.append((node.right, False))
    return best
