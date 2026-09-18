# Greedy: process points in weight order, push each just past the previous group's furthest position.
from typing import List


def getMinOperations2(weight: List[int], dist: List[int]) -> int:
    n = len(weight)
    order = sorted(range(n), key=lambda i: weight[i])
    total = 0
    prev = -1  # max position occupied by all strictly smaller weights
    i = 0
    while i < n:
        j = i
        w = weight[order[i]]
        while j < n and weight[order[j]] == w:
            j += 1
        group_max = prev
        for t in range(i, j):
            idx = order[t]
            pos = idx
            if pos <= prev:
                need = prev + 1 - pos
                d = dist[idx]
                k = (need + d - 1) // d
                total += k
                pos += k * d
            if pos > group_max:
                group_max = pos
        prev = group_max
        i = j
    return total
