# Bitmask DP over valid words: keep every reachable mask with its best total length.
from typing import List, Optional, Any


def maxUniqueCharacterSubsetLength(words: List[str]) -> int:
    masks = []
    for w in words:
        m = 0
        ok = True
        for ch in w:
            b = 1 << (ord(ch) - 97)
            if m & b:
                ok = False
                break
            m |= b
        if ok:
            masks.append(m)

    reachable = {0: 0}
    best = 0
    for m in masks:
        bits = bin(m).count("1")
        for cur, ln in list(reachable.items()):
            if cur & m:
                continue
            nxt = cur | m
            nl = ln + bits
            if nl > reachable.get(nxt, -1):
                reachable[nxt] = nl
                if nl > best:
                    best = nl
    return best
