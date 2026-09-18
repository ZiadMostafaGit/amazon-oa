# Approach: backtracking over sorted character counts, emitting each distinct permutation in lexicographic order.
from typing import List


def solve(s: str) -> List[str]:
    from collections import Counter

    counts = sorted(Counter(s).items())
    n = len(s)
    res: List[str] = []
    buf: List[str] = []
    items = [[ch, c] for ch, c in counts]

    def back() -> None:
        if len(buf) == n:
            res.append("".join(buf))
            return
        for pair in items:
            if pair[1] == 0:
                continue
            pair[1] -= 1
            buf.append(pair[0])
            back()
            buf.pop()
            pair[1] += 1

    if n:
        back()
    else:
        res.append("")
    return res
