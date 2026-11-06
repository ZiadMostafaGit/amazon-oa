# DFS that carries the path so far down to each child; a leaf emits it. Explicit stack, right pushed first
# so the left subtree is finished before the right one.
from typing import List, Optional, Any


def binaryTreePaths(root: Optional["TreeNode"]) -> List[str]:
    if root is None:
        return []
    out = []
    stack = [(root, str(root.val))]
    while stack:
        node, path = stack.pop()
        if node.left is None and node.right is None:
            out.append(path)
            continue
        if node.right is not None:
            stack.append((node.right, path + "->" + str(node.right.val)))
        if node.left is not None:
            stack.append((node.left, path + "->" + str(node.left.val)))
    return out
