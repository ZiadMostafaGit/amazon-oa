# Classic 1D DP over s2 index: dp[j] = s3[:i+j] is an interleaving of s1[:i] and s2[:j].
def solve(s1: str, s2: str, s3: str) -> bool:
    n, m = len(s1), len(s2)
    if n + m != len(s3):
        return False
    dp = [False] * (m + 1)
    dp[0] = True
    for j in range(1, m + 1):
        dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]
    for i in range(1, n + 1):
        dp[0] = dp[0] and s1[i - 1] == s3[i - 1]
        for j in range(1, m + 1):
            dp[j] = (dp[j] and s1[i - 1] == s3[i + j - 1]) or (dp[j - 1] and s2[j - 1] == s3[i + j - 1])
    return dp[m]
