# Run-length encode typed and each dictionary word, then compare run letters and counts.
from typing import List, Optional, Any


def _runs(s: str):
    out = []
    for ch in s:
        if out and out[-1][0] == ch:
            out[-1][1] += 1
        else:
            out.append([ch, 1])
    return out


def expandedWordMatches(typed: str, dictionary: List[str]) -> List[str]:
    base = _runs(typed)
    result = []
    for word in dictionary:
        runs = _runs(word)
        if len(runs) != len(base):
            continue
        if all(a[0] == b[0] and 1 <= a[1] <= b[1] for a, b in zip(runs, base)):
            result.append(word)
    return result
