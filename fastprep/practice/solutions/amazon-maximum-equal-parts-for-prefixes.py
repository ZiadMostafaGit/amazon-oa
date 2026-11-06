# Parts are contiguous. A prefix with letter counts c = g * v (g = gcd, v primitive) splits into k
# equal parts iff k | g and the prefixes with counts s*v, 2s*v, ..., g*v (s = g/k) all occur.
# Every prefix whose counts are a multiple of v is recorded under key v by its multiplier t;
# reach[v][s] = how many consecutive multiples s, 2s, ... have appeared. O(n * (26 + d(n))).
from math import gcd
from typing import List


def maximumEqualParts(packages: str) -> List[int]:
    n = len(packages)
    divs = [[] for _ in range(n + 1)]
    for d in range(1, n + 1):
        for m in range(d, n + 1, d):
            divs[m].append(d)
    counts = [0] * 26
    reach = {}
    res = []
    for ch in packages:
        counts[ord(ch) - 65] += 1
        g = 0
        for c in counts:
            if c:
                g = gcd(g, c)
        key = tuple(c // g for c in counts)
        r = reach.get(key)
        if r is None:
            r = reach[key] = {}
        best = 1
        for s in divs[g]:  # ascending, so the first full chain gives the most parts
            q = g // s
            if r.get(s, 0) == q - 1:
                r[s] = q
                if best == 1:
                    best = q
        res.append(best)
    return res
