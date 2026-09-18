# Linear DP over split points: dp[i] = ways to split prefix, only O(len(str(c))) candidate pieces per index.
def countArrays(n: int, c: int, k: int, s: str) -> int:
    mod = 10 ** k
    maxlen = len(str(c))
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, n + 1):
        total = 0
        lo = max(0, i - maxlen)
        for j in range(i - 1, lo - 1, -1):
            if dp[j] == 0:
                continue
            piece = s[j:i]
            if piece[0] == '0' and len(piece) > 1:
                continue
            if int(piece) > c:
                continue
            total += dp[j]
        dp[i] = total % mod
    return dp[n] % mod
