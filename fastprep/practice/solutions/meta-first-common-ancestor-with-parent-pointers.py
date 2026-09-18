# Depth equalization by walking parent pointers, then lock-step ascent (O(1) auxiliary space).
from typing import List, Optional, Any


def _depth(parent: List[int], node: int) -> int:
    d = 0
    while parent[node] != -1:
        node = parent[node]
        d += 1
    return d


def firstCommonAncestor(parent: List[int], first: int, second: int) -> int:
    a, b = first, second
    da, db = _depth(parent, a), _depth(parent, b)
    while da > db:
        a = parent[a]
        da -= 1
    while db > da:
        b = parent[b]
        db -= 1
    while a != b:
        a = parent[a]
        b = parent[b]
    return a
