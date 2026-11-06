# A plain (unbalanced) BST built from scratch: each operation walks one root-to-node path by the ordering.
# Deletion of a two-child node copies in the inorder successor and deletes that instead.
from typing import List


class _Node:
    __slots__ = ("key", "left", "right")

    def __init__(self, key):
        self.key, self.left, self.right = key, None, None


def bstOperations(operations: List[List[int]]) -> List[int]:
    root = None
    out = []

    def insert(key):
        nonlocal root
        if root is None:
            root = _Node(key)
            return
        cur = root
        while True:
            if key == cur.key:
                return
            side = "left" if key < cur.key else "right"
            nxt = getattr(cur, side)
            if nxt is None:
                setattr(cur, side, _Node(key))
                return
            cur = nxt

    def search(key):
        cur = root
        while cur is not None:
            if key == cur.key:
                return True
            cur = cur.left if key < cur.key else cur.right
        return False

    def delete(key):
        nonlocal root
        parent, cur = None, root
        while cur is not None and cur.key != key:
            parent, cur = cur, (cur.left if key < cur.key else cur.right)
        if cur is None:
            return
        if cur.left is not None and cur.right is not None:
            sp, s = cur, cur.right
            while s.left is not None:
                sp, s = s, s.left
            cur.key = s.key
            parent, cur = sp, s          # now remove the successor, which has no left child
        child = cur.left if cur.left is not None else cur.right
        if parent is None:
            root = child
        elif parent.left is cur:
            parent.left = child
        else:
            parent.right = child

    for op, key in operations:
        if op == 0:
            insert(key)
        elif op == 1:
            out.append(1 if search(key) else 0)
        else:
            delete(key)
    return out
