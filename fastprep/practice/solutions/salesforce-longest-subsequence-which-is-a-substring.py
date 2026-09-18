# DP over (prefix of x, end position in y): contiguous in y, skippable in x.
def longestSubsequenceWhichIsSubstring(x: str, y: str) -> int:
    n, m = len(x), len(y)
    prev = [0] * (m + 1)
    best = 0
    for i in range(1, n + 1):
        cur = [0] * (m + 1)
        xc = x[i - 1]
        for j in range(1, m + 1):
            if xc == y[j - 1]:
                v = prev[j - 1] + 1
            else:
                v = prev[j]
            cur[j] = v
            if v > best:
                best = v
        prev = cur
    return best
