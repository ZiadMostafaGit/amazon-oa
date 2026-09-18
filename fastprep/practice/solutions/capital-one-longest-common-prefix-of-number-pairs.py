# Trie-free approach: store every prefix of arr1 values in a set, then probe prefixes of arr2 values.
from typing import List


def longestCommonPrefixLength(arr1: List[int], arr2: List[int]) -> int:
    prefixes = set()
    for v in arr1:
        s = str(v)
        for i in range(1, len(s) + 1):
            prefixes.add(s[:i])
    best = 0
    for v in arr2:
        s = str(v)
        for i in range(1, len(s) + 1):
            if s[:i] in prefixes:
                if i > best:
                    best = i
            else:
                break
    return best
