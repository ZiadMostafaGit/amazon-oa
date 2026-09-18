# Counting: a reversal is uniquely identified by its first/last mismatching endpoints, so count unequal-character pairs.
from collections import Counter


def findNumberOfPossibleUniqueStrings(s: str) -> int:
    n = len(s)
    total = n * (n - 1) // 2
    for cnt in Counter(s).values():
        total -= cnt * (cnt - 1) // 2
    return total + 1
