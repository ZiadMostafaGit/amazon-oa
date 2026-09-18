# Counting: every reversal shrinks to a canonical interval [i,j] with s[i]!=s[j] (or empty);
# each such interval yields a unique string, so answer = 1 + #{i<j : s[i]!=s[j]}.
from collections import Counter


def countDistinctPasswords(password: str) -> int:
    n = len(password)
    total_pairs = n * (n - 1) // 2
    same_pairs = 0
    for c in Counter(password).values():
        same_pairs += c * (c - 1) // 2
    return 1 + total_pairs - same_pairs
