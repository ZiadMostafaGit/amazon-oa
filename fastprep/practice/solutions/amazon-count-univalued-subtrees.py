# Iterative post-order DFS; a subtree is uni-valued when both children are and their values match.
from typing import Optional, Any


def solve(root: Optional["TreeNode"]) -> int:
    if root is None:
        return 0

    count = 0
    uni = {}  # id(node) -> bool

    stack = [(root, False)]
    while stack:
        node, processed = stack.pop()
        if not processed:
            stack.append((node, True))
            if node.left is not None:
                stack.append((node.left, False))
            if node.right is not None:
                stack.append((node.right, False))
        else:
            ok = True
            if node.left is not None:
                if not uni[id(node.left)] or node.left.val != node.val:
                    ok = False
            if node.right is not None:
                if not uni[id(node.right)] or node.right.val != node.val:
                    ok = False
            uni[id(node)] = ok
            if ok:
                count += 1

    return count
