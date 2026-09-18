# Greedy two-pointer subsequence match where each new char matches itself or its cyclic successor.
from typing import List, Optional, Any


def checkSimilarPasswords(newPasswords: List[str], oldPasswords: List[str]) -> List[str]:
    res = []
    for new, old in zip(newPasswords, oldPasswords):
        i = 0
        n = len(new)
        for c in old:
            while i < n:
                nc = new[i]
                i += 1
                if nc == c or chr((ord(nc) - 97 + 1) % 26 + 97) == c:
                    break
            else:
                break
        else:
            res.append("YES")
            continue
        res.append("NO")
    return res
