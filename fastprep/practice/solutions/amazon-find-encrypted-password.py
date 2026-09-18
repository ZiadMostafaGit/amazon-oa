# Counting sort of half the multiset: smallest half ascending + odd-count middle + its mirror.
from collections import Counter


def findEncryptedPassword(password: str) -> str:
    cnt = Counter(password)
    half = []
    middle = ""
    for ch in sorted(cnt):
        half.append(ch * (cnt[ch] // 2))
        if cnt[ch] % 2 == 1:
            middle = ch
    first = "".join(half)
    return first + middle + first[::-1]
