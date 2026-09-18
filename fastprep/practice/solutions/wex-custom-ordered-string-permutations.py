# Backtracking over the sorted multiset of characters, using a custom rank (digits < lowercase < uppercase).
from typing import List, Optional, Any


def _rank(c: str) -> int:
    if c.isdigit():
        return ord(c) - ord('0')
    if 'a' <= c <= 'z':
        return 10 + ord(c) - ord('a')
    return 36 + ord(c) - ord('A')


def sortedPermutations(s: str) -> List[str]:
    chars = sorted(s, key=_rank)
    n = len(chars)
    used = [False] * n
    out: List[str] = []
    cur: List[str] = []

    def bt() -> None:
        if len(cur) == n:
            out.append("".join(cur))
            return
        for i in range(n):
            if used[i]:
                continue
            # skip duplicates: only take the first unused copy of a run of equal chars
            if i > 0 and chars[i] == chars[i - 1] and not used[i - 1]:
                continue
            used[i] = True
            cur.append(chars[i])
            bt()
            cur.pop()
            used[i] = False

    bt()
    return out
