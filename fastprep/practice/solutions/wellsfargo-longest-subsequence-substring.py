def longestSubsequence(x: str, y: str) -> int:
    m = len(y)
    # prev[j]: longest suffix of y[:j] that is a subsequence of the x prefix so far
    prev = [0] * (m + 1)
    best = 0
    for c in x:
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            if y[j - 1] == c:
                v = prev[j - 1] + 1
                cur[j] = v if v > prev[j] else prev[j]
            else:
                cur[j] = prev[j]
        prev = cur
        mx = max(cur)
        if mx > best:
            best = mx
    return best
