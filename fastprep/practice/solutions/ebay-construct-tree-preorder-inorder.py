# The next preorder value is the root of the current range; its inorder position splits the range into
# left and right subtrees. A value -> inorder index map makes each split O(1): O(n) overall.
import sys
from typing import List, Optional, Any

sys.setrecursionlimit(10000)


def buildTree(preorder: List[int], inorder: List[int]) -> Optional["TreeNode"]:
    pos = {v: i for i, v in enumerate(inorder)}
    nxt = 0

    def build(lo, hi):
        nonlocal nxt
        if lo > hi:
            return None
        val = preorder[nxt]
        nxt += 1
        node = TreeNode(val)
        mid = pos[val]
        node.left = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(inorder) - 1)
