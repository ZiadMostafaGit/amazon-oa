# The inorder sequence of a BST is sorted; two swapped values show up as one or two descents in it.
# The first descent's larger value and the last descent's smaller value are the swapped pair.
from typing import Optional, Any


def recoverTree(root: Optional["TreeNode"]) -> Optional["TreeNode"]:
    first = second = prev = None
    stack, node = [], root
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if prev is not None and prev.val > node.val:
            if first is None:
                first = prev
            second = node
        prev = node
        node = node.right
    if first is not None:
        first.val, second.val = second.val, first.val
    return root
