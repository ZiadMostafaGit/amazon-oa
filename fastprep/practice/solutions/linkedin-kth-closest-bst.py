# In-order walk gives sorted values; expand two pointers outward from target.
from typing import Optional, Any
from bisect import bisect_left


def kthClosest(root: Optional["TreeNode"], target: int, k: int) -> int:
    vals = []
    stack, node = [], root
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = node.left
        node = stack.pop()
        vals.append(node.val)
        node = node.right
    j = bisect_left(vals, target)  # vals[j] >= target
    i = j - 1                      # vals[i] < target
    ans = None
    for _ in range(k):
        # ties go to the smaller value, which is the left side
        if i >= 0 and (j >= len(vals) or target - vals[i] <= vals[j] - target):
            ans = vals[i]
            i -= 1
        else:
            ans = vals[j]
            j += 1
    return ans
