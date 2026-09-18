# Divide and conquer on inorder ranges: the root of a range is the value with the smallest
# level-order position, found with a sparse-table range-minimum query; built with an explicit stack.
from typing import List, Optional, Any


def solve(levelOrder: List[int], inorder: List[int]) -> Optional["TreeNode"]:
    n = len(inorder)
    if n == 0:
        return None

    level_pos = {v: i for i, v in enumerate(levelOrder)}
    # pos[i] = level-order position of the value sitting at inorder index i
    pos = [level_pos[v] for v in inorder]

    # Sparse table storing the inorder index that minimises pos.
    LOG = [0] * (n + 1)
    for i in range(2, n + 1):
        LOG[i] = LOG[i >> 1] + 1
    levels = LOG[n] + 1
    table = [list(range(n))]
    k = 1
    while (1 << k) <= n:
        prev = table[k - 1]
        span = 1 << (k - 1)
        cur = [0] * (n - (1 << k) + 1)
        for i in range(len(cur)):
            a = prev[i]
            b = prev[i + span]
            cur[i] = a if pos[a] <= pos[b] else b
        table.append(cur)
        k += 1

    def rmq(lo: int, hi: int) -> int:
        j = LOG[hi - lo + 1]
        a = table[j][lo]
        b = table[j][hi - (1 << j) + 1]
        return a if pos[a] <= pos[b] else b

    root_idx = rmq(0, n - 1)
    root = TreeNode(inorder[root_idx])  # noqa: F821
    stack = [(root, 0, n - 1, root_idx)]
    while stack:
        node, lo, hi, mid = stack.pop()
        if lo <= mid - 1:
            j = rmq(lo, mid - 1)
            child = TreeNode(inorder[j])  # noqa: F821
            node.left = child
            stack.append((child, lo, mid - 1, j))
        if mid + 1 <= hi:
            j = rmq(mid + 1, hi)
            child = TreeNode(inorder[j])  # noqa: F821
            node.right = child
            stack.append((child, mid + 1, hi, j))
    return root
