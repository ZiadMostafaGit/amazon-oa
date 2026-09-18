# Approach: count character frequencies, then scan the string for the first count-one character.
from collections import Counter


def solve(s: str) -> str:
    freq = Counter(s)
    for ch in s:
        if freq[ch] == 1:
            return ch
    return ""
