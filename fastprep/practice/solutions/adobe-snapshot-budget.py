from typing import List


def minimumSnapshots(n: int, maxCost: int, parents: List[int]) -> int:
    # far[v] = distance from v down to its deepest descendant that is not yet
    # covered by a snapshot inside v's subtree (-1 when nothing is pending).
    far = [0] * (n + 1)
    count = 0
    for v in range(n, 0, -1):
        if far[v] >= maxCost:
            count += 1  # the deepest pending node is exactly maxCost below v
            far[v] = -1
        p = parents[v - 1]
        if far[v] + 1 > far[p]:
            far[p] = far[v] + 1
    return count
