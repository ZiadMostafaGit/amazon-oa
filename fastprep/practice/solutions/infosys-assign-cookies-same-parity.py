# Parity splits the problem into two independent classic assign-cookies instances; greedy two-pointer on each.
from typing import List, Optional, Any


def _greedy(children: List[int], cookies: List[int]) -> int:
    children.sort()
    cookies.sort()
    i = j = count = 0
    while i < len(children) and j < len(cookies):
        if cookies[j] >= children[i]:
            count += 1
            i += 1
        j += 1
    return count


def findContentChildren(g: List[int], s: List[int]) -> int:
    g_odd = [x for x in g if x & 1]
    g_even = [x for x in g if not x & 1]
    s_odd = [x for x in s if x & 1]
    s_even = [x for x in s if not x & 1]
    return _greedy(g_odd, s_odd) + _greedy(g_even, s_even)
