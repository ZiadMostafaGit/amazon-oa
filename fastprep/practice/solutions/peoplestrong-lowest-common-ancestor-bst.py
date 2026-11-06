# Walk down from the root: while both targets are on the same side, go that way; the first split point is the LCA.
from typing import Optional, Any


def lcaBstValue(root: Optional["TreeNode"], p: int, q: int) -> int:
    lo, hi = min(p, q), max(p, q)
    node = root
    while node is not None:
        if hi < node.val:
            node = node.left
        elif lo > node.val:
            node = node.right
        else:
            return node.val
    return -1
