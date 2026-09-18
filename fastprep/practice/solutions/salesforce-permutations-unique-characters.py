# Backtracking over sorted characters, which emits permutations in lexicographic order.
from typing import List, Optional, Any


def generatePermutations(word: str) -> List[str]:
    chars = sorted(word)
    n = len(chars)
    used = [False] * n
    cur = []
    out = []

    def backtrack():
        if len(cur) == n:
            out.append("".join(cur))
            return
        for i in range(n):
            if used[i]:
                continue
            used[i] = True
            cur.append(chars[i])
            backtrack()
            cur.pop()
            used[i] = False

    backtrack()
    return out
