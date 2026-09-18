# Sliding window with a need-count map and a counter of still-missing characters.
from collections import Counter


def solve(s: str, t: str) -> str:
    if not s or not t or len(t) > len(s):
        return ""
    need = Counter(t)
    missing = len(t)
    best_len = len(s) + 1
    best_start = 0
    left = 0
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        while missing == 0:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_start = left
            lc = s[left]
            need[lc] += 1
            if need[lc] > 0:
                missing += 1
            left += 1
    return "" if best_len > len(s) else s[best_start:best_start + best_len]
