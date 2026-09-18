# Monotonic-stack BST construction from preorder, then iterative preorder serialization with '#' markers.
from typing import List, Optional, Any


class _Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val: int) -> None:
        self.val = val
        self.left = None
        self.right = None


def reconstructBST(preorder: List[int]) -> str:
    if not preorder:
        return "#"
    root = _Node(preorder[0])
    stack = [root]
    for v in preorder[1:]:
        node = _Node(v)
        parent = None
        while stack and stack[-1].val < v:
            parent = stack.pop()
        if parent is not None:
            parent.right = node
        else:
            stack[-1].left = node
        stack.append(node)

    out = []
    work = [root]
    while work:
        cur = work.pop()
        if cur is None:
            out.append("#")
            continue
        out.append(str(cur.val))
        work.append(cur.right)
        work.append(cur.left)
    return ",".join(out)
