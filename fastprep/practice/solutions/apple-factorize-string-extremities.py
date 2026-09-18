# KMP streaming: longest suffix of the first string that is a prefix of the second, both orders.
def _overlap(a: str, b: str) -> int:
    # longest k <= min(len(a), len(b)) with a[-k:] == b[:k]
    if not a or not b:
        return 0
    m = len(b)
    fail = [0] * m
    k = 0
    for i in range(1, m):
        c = b[i]
        while k and c != b[k]:
            k = fail[k - 1]
        if c == b[k]:
            k += 1
        fail[i] = k
    j = 0
    last = len(a) - 1
    for i, c in enumerate(a):
        while j and c != b[j]:
            j = fail[j - 1]
        if c == b[j]:
            j += 1
        if j == m:
            if i == last:
                return m
            j = fail[j - 1]
    return j


def factorizeExtremities(str1: str, str2: str) -> str:
    k1 = _overlap(str1, str2)
    k2 = _overlap(str2, str1)
    if k1 >= k2:
        return str1 + str2[k1:]
    return str2 + str1[k2:]
