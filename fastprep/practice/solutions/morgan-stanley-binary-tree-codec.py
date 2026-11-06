# Preorder with -1 null markers; decode with a cursor that rebuilds child links.
from typing import List, Optional, Any
from collections import deque


class _Node:
    __slots__ = ("val", "left", "right")

    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def treeCodec(root: Optional["TreeNode"], encoded: List[int]) -> List[List[int]]:
    ser = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            ser.append(-1)
            continue
        ser.append(node.val)
        stack.append(node.right)
        stack.append(node.left)

    # iterative preorder decoder: stack of (node, which child slot is next)
    it = iter(encoded)
    first = next(it)
    new_root = None
    if first != -1:
        new_root = _Node(first)
        st = [[new_root, 0]]
        for tok in it:
            while st and st[-1][1] == 2:
                st.pop()
            top = st[-1]
            child = None if tok == -1 else _Node(tok)
            if top[1] == 0:
                top[0].left = child
            else:
                top[0].right = child
            top[1] += 1
            if top[1] == 2:
                st.pop()
            if child is not None:
                st.append([child, 0])

    lvl = []
    if new_root is not None:
        q = deque([new_root])
        lvl.append(new_root.val)
        while q:
            n = q.popleft()
            for c in (n.left, n.right):
                if c is None:
                    lvl.append(-1)
                else:
                    lvl.append(c.val)
                    q.append(c)
        while lvl and lvl[-1] == -1:
            lvl.pop()
    return [ser, lvl]
