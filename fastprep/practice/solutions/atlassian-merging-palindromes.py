# Counting: take every character pair from each string independently, sort the half, and place the smallest leftover odd character in the center.
from collections import Counter


def mergingPalindromes(first: str, second: str) -> str:
    c1 = Counter(first)
    c2 = Counter(second)
    pairs = Counter()
    odd_chars = set()
    for cnt in (c1, c2):
        for ch, k in cnt.items():
            if k // 2:
                pairs[ch] += k // 2
            if k % 2:
                odd_chars.add(ch)
    half_parts = []
    for ch in sorted(pairs):
        half_parts.append(ch * pairs[ch])
    half = ''.join(half_parts)
    center = min(odd_chars) if odd_chars else ''
    return half + center + half[::-1]
