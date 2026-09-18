# Counting: sort half of the multiset of letters, mirror it, keep the odd letter (if any) in the middle.
from collections import Counter


def computeEncodedProductName(nameString: str) -> str:
    cnt = Counter(nameString)
    half = []
    middle = ''
    for ch in sorted(cnt):
        c = cnt[ch]
        if c % 2:
            middle = ch
        half.append(ch * (c // 2))
    first = ''.join(half)
    return first + middle + first[::-1]
