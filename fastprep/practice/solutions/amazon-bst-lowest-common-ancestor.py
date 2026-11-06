# In a BST built by insertion, the LCA of p and q is the first inserted value lying between them:
# until such a value arrives, p and q always fall on the same side of every node; that value is where they split.
from typing import List


def bstLowestCommonAncestor(insertionOrder: List[int], p: int, q: int) -> int:
    lo, hi = min(p, q), max(p, q)
    for v in insertionOrder:
        if lo <= v <= hi:
            return v
    return -1
