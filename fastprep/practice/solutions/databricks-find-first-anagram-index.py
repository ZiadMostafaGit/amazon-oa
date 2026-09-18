# Fixed-size sliding window over character counts, tracking how many letters match.
def findFirstAnagramIndex(s: str, pattern: str) -> int:
    m = len(pattern)
    n = len(s)
    if m == 0:
        return 0
    if m > n:
        return -1
    need = [0] * 26
    for c in pattern:
        need[ord(c) - 97] += 1
    have = [0] * 26
    for i in range(m):
        have[ord(s[i]) - 97] += 1
    if have == need:
        return 0
    for i in range(m, n):
        have[ord(s[i]) - 97] += 1
        have[ord(s[i - m]) - 97] -= 1
        if have == need:
            return i - m + 1
    return -1
