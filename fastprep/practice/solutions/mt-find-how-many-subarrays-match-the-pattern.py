from typing import List, Optional, Any


def findHowManySubarraysMatchThePattern(numbers: List[int], pattern: List[int]) -> int:
    # turn neighbours into a sign string, then count occurrences of pattern (KMP)
    signs = []
    for i in range(1, len(numbers)):
        d = numbers[i] - numbers[i - 1]
        signs.append((d > 0) - (d < 0))
    m = len(pattern)
    if m == 0:
        return len(numbers)
    fail = [0] * m
    k = 0
    for i in range(1, m):
        while k and pattern[i] != pattern[k]:
            k = fail[k - 1]
        if pattern[i] == pattern[k]:
            k += 1
        fail[i] = k
    count = 0
    k = 0
    for s in signs:
        while k and s != pattern[k]:
            k = fail[k - 1]
        if s == pattern[k]:
            k += 1
        if k == m:
            count += 1
            k = fail[k - 1]
    return count
