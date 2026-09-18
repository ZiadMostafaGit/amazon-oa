# Iterative inorder traversal to get sorted keys, prefix sums + binary search per query.
from typing import List, Optional, Any
import bisect


def rangeAggregates(root: Optional[TreeNode], queries: List[List[int]]) -> List[List[float]]:
    keys = []
    stack = []
    node = root
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        keys.append(node.val)
        node = node.right

    prefix = [0] * (len(keys) + 1)
    for i, v in enumerate(keys):
        prefix[i + 1] = prefix[i] + v

    out = []
    for q in queries:
        low, high = q[0], q[1]
        i = bisect.bisect_left(keys, low)
        j = bisect.bisect_right(keys, high)
        cnt = j - i
        if cnt <= 0:
            out.append([0.0, 0.0])
        else:
            s = prefix[j] - prefix[i]
            out.append([float(s), s / cnt])
    return out
