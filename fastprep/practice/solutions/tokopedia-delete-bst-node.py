# Approach: iterative BST search, then canonical inorder-successor replacement for two-child nodes.
from typing import Optional, Any


def deleteNode(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    if root is None:
        return None
    if key < root.val:
        root.left = deleteNode(root.left, key)
    elif key > root.val:
        root.right = deleteNode(root.right, key)
    else:
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        succ = root.right
        while succ.left is not None:
            succ = succ.left
        root.val = succ.val
        root.right = deleteNode(root.right, succ.val)
    return root
