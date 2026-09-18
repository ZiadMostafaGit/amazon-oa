# BST descent: track the last node taken as a left turn; if target has a right subtree use its leftmost node.
from typing import Optional, Any


def findInorderSuccessor(root: Optional[TreeNode], targetValue: int) -> int:
    successor = None
    node = root
    target = None
    while node is not None:
        if targetValue < node.val:
            successor = node
            node = node.left
        elif targetValue > node.val:
            node = node.right
        else:
            target = node
            break

    if target is not None and target.right is not None:
        cur = target.right
        while cur.left is not None:
            cur = cur.left
        return cur.val

    return successor.val if successor is not None else -1
