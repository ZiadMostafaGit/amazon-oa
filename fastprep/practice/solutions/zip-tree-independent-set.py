# Tree DP: take[v] = value + sum skip[children]; skip[v] = sum max(take, skip) of children.
# Parents appear before children, so a reverse scan is a post-order.
from typing import List


def maxTreeSum(nodes: List[List[int]]) -> int:
    n = len(nodes)
    take = [v for v, _ in nodes]
    skip = [0] * n
    for i in range(n - 1, 0, -1):
        p = nodes[i][1]
        take[p] += skip[i]
        skip[p] += max(take[i], skip[i])
    return max(take[0], skip[0])
