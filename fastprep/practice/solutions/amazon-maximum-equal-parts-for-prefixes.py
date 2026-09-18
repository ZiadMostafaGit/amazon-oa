# Running character counts; answer for each prefix is gcd of the 26 letter frequencies.
from math import gcd
from typing import List


def maximumEqualParts(packages: str) -> List[int]:
    counts = [0] * 26
    res = []
    for ch in packages:
        counts[ord(ch) - 65] += 1
        g = 0
        for c in counts:
            if c:
                g = gcd(g, c)
                if g == 1:
                    break
        res.append(g if g else 1)
    return res
