# Iterative preorder traversal with an explicit stack, joined by commas.
from typing import Optional, Any


def serializeBST(root: Optional["TreeNode"]) -> str:
    if root is None:
        return ""
    out = []
    stack = [root]
    while stack:
        node = stack.pop()
        out.append(str(node.val))
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return ",".join(out)
