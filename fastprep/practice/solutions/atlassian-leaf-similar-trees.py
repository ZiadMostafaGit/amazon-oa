# Iterative DFS collecting each tree's left-to-right leaf sequence, then comparing them.
from typing import List, Optional


def _leaves(root: Optional["TreeNode"]) -> List[int]:
    seq: List[int] = []
    if root is None:
        return seq
    stack = [root]
    while stack:
        node = stack.pop()
        if node.left is None and node.right is None:
            seq.append(node.val)
            continue
        # push right first so the left subtree is visited first
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return seq


def leafSimilar(root1: Optional["TreeNode"], root2: Optional["TreeNode"]) -> bool:
    return _leaves(root1) == _leaves(root2)
