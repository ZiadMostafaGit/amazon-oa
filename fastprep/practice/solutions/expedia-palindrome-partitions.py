# Backtrack over the end of the next piece; only recurse when the piece is a palindrome.
from typing import List, Optional, Any


def palindromePartitions(text: str) -> List[List[str]]:
    n = len(text)
    out = []
    cur = []

    def go(start):
        if start == n:
            out.append(list(cur))
            return
        for end in range(start + 1, n + 1):
            piece = text[start:end]
            if piece == piece[::-1]:
                cur.append(piece)
                go(end)
                cur.pop()

    go(0)
    out.sort()
    return out
