# Build a child-list forest keyed by parent id, then emit an iterative preorder walk with 2-space indentation.
from typing import List, Optional, Any


def renderCommentHierarchy(ids: List[int], parentIds: List[int], texts: List[str]) -> List[str]:
    n = len(ids)
    children = {}
    roots = []
    for i in range(n):
        p = parentIds[i]
        if p == -1:
            roots.append(i)
        else:
            children.setdefault(p, []).append(i)
    out = []
    # stack holds (index, depth); push children reversed so input order is preserved
    stack = [(roots[k], 0) for k in range(len(roots) - 1, -1, -1)]
    while stack:
        i, d = stack.pop()
        out.append("  " * d + texts[i])
        kids = children.get(ids[i])
        if kids:
            for k in range(len(kids) - 1, -1, -1):
                stack.append((kids[k], d + 1))
    return out
