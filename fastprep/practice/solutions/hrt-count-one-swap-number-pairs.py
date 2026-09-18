# Group equal values, then for each distinct value enumerate its one-swap variants and match counts.
from typing import List
from collections import Counter


def _variants(value: int):
    s = str(value)
    n = len(s)
    out = set()
    for i in range(n):
        for j in range(i + 1, n):
            if s[i] == s[j]:
                continue
            chars = list(s)
            chars[i], chars[j] = chars[j], chars[i]
            if chars[0] == '0':
                continue
            out.add(int(''.join(chars)))
    out.discard(value)
    return out


def countOneSwapPairs(numbers: List[int]) -> int:
    freq = Counter(numbers)
    total = 0
    for value, count in freq.items():
        total += count * (count - 1) // 2
        for other in _variants(value):
            if other > value and other in freq:
                total += count * freq[other]
    return total
