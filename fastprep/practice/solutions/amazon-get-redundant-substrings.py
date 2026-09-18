# Prefix sums + hash map: condition reduces to (a-1)*V + (b-1)*C == 0 over a substring.
from collections import defaultdict


def getRedundantSubstrings(word: str, a: int, b: int) -> int:
    p = a - 1
    q = b - 1
    vowels = set("aeiou")
    seen = defaultdict(int)
    cur = 0
    seen[0] = 1
    total = 0
    for ch in word:
        cur += p if ch in vowels else q
        total += seen[cur]
        seen[cur] += 1
    return total
