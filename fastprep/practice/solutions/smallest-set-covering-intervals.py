# Greedy: sort by end ascending (start descending) and keep the two largest chosen points.
from typing import List


def interval(first: List[int], last: List[int]) -> int:
    intervals = sorted(zip(first, last), key=lambda iv: (iv[1], -iv[0]))
    count = 0
    # a < b are the two largest points chosen so far
    a = b = float("-inf")
    for s, e in intervals:
        if s > b:
            # no chosen point inside: take the two rightmost integers
            a, b = e - 1, e
            count += 2
        elif s > a:
            # exactly one chosen point (b) inside: add the rightmost integer
            a, b = b, e
            count += 1
    return count
