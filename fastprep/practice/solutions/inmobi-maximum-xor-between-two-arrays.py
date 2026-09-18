# Binary trie over arr2; query each value of arr1 greedily for the max XOR.
from typing import List, Optional, Any

BITS = 30


def maximumXorBetweenArrays(arr1: List[int], arr2: List[int]) -> int:
    root = [None, None]
    for v in arr2:
        node = root
        for i in range(BITS, -1, -1):
            b = (v >> i) & 1
            if node[b] is None:
                node[b] = [None, None]
            node = node[b]
    best = 0
    for v in arr1:
        node = root
        cur = 0
        for i in range(BITS, -1, -1):
            b = (v >> i) & 1
            want = 1 - b
            if node[want] is not None:
                cur |= 1 << i
                node = node[want]
            else:
                node = node[b]
        if cur > best:
            best = cur
    return best
