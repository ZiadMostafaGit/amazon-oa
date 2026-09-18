from typing import List, Optional, Any

INF = float("inf")


def solve(leftChild: List[int], rightChild: List[int], leftCost: List[int], rightCost: List[int]) -> int:
    n = len(leftChild) if leftChild is not None else 0
    if n == 0:
        return 0

    # f[v] = cheapest cost to disconnect v from every original leaf inside its
    # own subtree, cutting only edges strictly below v.  A leaf has no such
    # edges, so it is impossible from below -> INF (its parent edge must pay).
    f = [0] * n

    # iterative post-order so deep/degenerate trees do not blow the stack
    stack = [(0, False)]
    while stack:
        node, processed = stack.pop()
        if node == -1:
            continue
        if not processed:
            stack.append((node, True))
            lc = leftChild[node]
            rc = rightChild[node]
            if lc != -1:
                stack.append((lc, False))
            if rc != -1:
                stack.append((rc, False))
            continue

        lc = leftChild[node]
        rc = rightChild[node]
        if lc == -1 and rc == -1:
            f[node] = INF
            continue
        total = 0
        if lc != -1:
            total += min(leftCost[node], f[lc])
        if rc != -1:
            total += min(rightCost[node], f[rc])
        f[node] = total

    root = f[0]
    return 0 if root == INF else int(root)
