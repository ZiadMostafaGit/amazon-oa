# Decode the compact BFS array, then iterative post-order DP on best downward gain per node.
from typing import List, Optional, Any

MISSING = -1001


def maxPathSum(levelOrder: List[int]) -> int:
    n = len(levelOrder)
    val = [levelOrder[0]]
    left = [-1]
    right = [-1]
    queue = [0]
    head = 0
    i = 1
    while head < len(queue) and i < n:
        cur = queue[head]
        head += 1
        if i < n:
            v = levelOrder[i]
            i += 1
            if v != MISSING:
                val.append(v)
                left.append(-1)
                right.append(-1)
                idx = len(val) - 1
                left[cur] = idx
                queue.append(idx)
        if i < n:
            v = levelOrder[i]
            i += 1
            if v != MISSING:
                val.append(v)
                left.append(-1)
                right.append(-1)
                idx = len(val) - 1
                right[cur] = idx
                queue.append(idx)

    total = len(val)
    gain = [0] * total
    best = float('-inf')
    stack = [(0, False)]
    while stack:
        node, expanded = stack.pop()
        if not expanded:
            stack.append((node, True))
            if left[node] != -1:
                stack.append((left[node], False))
            if right[node] != -1:
                stack.append((right[node], False))
        else:
            gl = gain[left[node]] if left[node] != -1 else 0
            gr = gain[right[node]] if right[node] != -1 else 0
            gl = gl if gl > 0 else 0
            gr = gr if gr > 0 else 0
            cur = val[node] + gl + gr
            if cur > best:
                best = cur
            gain[node] = val[node] + (gl if gl > gr else gr)
    return best
