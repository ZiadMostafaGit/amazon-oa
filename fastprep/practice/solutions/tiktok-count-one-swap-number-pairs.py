# Group equal values, then for each distinct value enumerate all one-swap digit variants and look them up in a counter.
from typing import List, Optional, Any
from collections import Counter


def countOneSwapPairs(numbers: List[int]) -> int:
    cnt = Counter(numbers)

    total = 0
    # pairs of identical numbers need no swap at all
    for c in cnt.values():
        total += c * (c - 1) // 2

    cross = 0
    for a, ca in cnt.items():
        s = str(a)
        n = len(s)
        seen = set()
        for i in range(n):
            for j in range(i + 1, n):
                if s[i] == s[j]:
                    continue
                if i == 0 and s[j] == '0':
                    continue  # swapped representation would start with 0
                lst = list(s)
                lst[i], lst[j] = lst[j], lst[i]
                seen.add(''.join(lst))
        acc = 0
        for t in seen:
            v = int(t)
            if v != a:
                acc += cnt.get(v, 0)
        cross += ca * acc

    return total + cross // 2
