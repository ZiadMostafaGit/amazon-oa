# O(n^2) palindrome DP table, then scan the two cut points.
def canSplitIntoThreePalindromes(s: str) -> bool:
    n = len(s)
    if n < 3:
        return False
    pal = [bytearray(n) for _ in range(n)]
    for i in range(n - 1, -1, -1):
        row = pal[i]
        row[i] = 1
        if i + 1 < n:
            nxt = pal[i + 1]
            if s[i] == s[i + 1]:
                row[i + 1] = 1
            for j in range(i + 2, n):
                if s[i] == s[j] and nxt[j - 1]:
                    row[j] = 1
    first = pal[0]
    last = n - 1
    for i in range(0, n - 2):
        if not first[i]:
            continue
        mid = pal[i + 1]
        for j in range(i + 1, n - 1):
            if mid[j] and pal[j + 1][last]:
                return True
    return False
