def findFirstOccurrence(haystack: str, needle: str) -> int:
    m = len(needle)
    if m == 0:
        return 0
    fail = [0] * m
    k = 0
    for i in range(1, m):
        while k and needle[i] != needle[k]:
            k = fail[k - 1]
        if needle[i] == needle[k]:
            k += 1
        fail[i] = k
    k = 0
    for i, ch in enumerate(haystack):
        while k and ch != needle[k]:
            k = fail[k - 1]
        if ch == needle[k]:
            k += 1
        if k == m:
            return i - m + 1
    return -1
