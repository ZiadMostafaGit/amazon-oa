# DP over interleavings: dp[i][j] = min inversions merging primary[:i] with secondary[:j],
# using prefix "count of characters strictly greater than c" tables for O(1) transitions.

def _greater_prefix(s: str):
    # g[i][c] = number of s[0:i] strictly greater than chr(ord('a')+c)
    n = len(s)
    g = [[0] * 26 for _ in range(n + 1)]
    for i, ch in enumerate(s):
        v = ord(ch) - 97
        row_prev = g[i]
        row = g[i + 1]
        for c in range(26):
            row[c] = row_prev[c] + (1 if v > c else 0)
    return g


def getMinimumConflicts(primary: str, secondary: str) -> int:
    n, m = len(primary), len(secondary)
    gp = _greater_prefix(primary)
    gs = _greater_prefix(secondary)
    pv = [ord(ch) - 97 for ch in primary]
    sv = [ord(ch) - 97 for ch in secondary]

    INF = float('inf')
    prev = [0] * (m + 1)
    # i = 0 row: only secondary chars placed
    for j in range(1, m + 1):
        c = sv[j - 1]
        prev[j] = prev[j - 1] + gs[j - 1][c]

    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        c = pv[i - 1]
        cur[0] = prev[0] + gp[i - 1][c]
        for j in range(1, m + 1):
            cp = pv[i - 1]
            a = prev[j] + gp[i - 1][cp] + gs[j][cp]
            cs = sv[j - 1]
            b = cur[j - 1] + gp[i][cs] + gs[j - 1][cs]
            cur[j] = a if a < b else b
        prev = cur
    return prev[m]
