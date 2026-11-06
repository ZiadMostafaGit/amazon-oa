# Interval DP on one string: dp[i][j] = longest palindromic subsequence of s[i..j].
def longestPalindromeSubseq(s: str) -> int:
    n = len(s)
    if n == 0:
        return 0
    dp = [0] * n                      # dp[j] holds the row for the current i
    for i in range(n - 1, -1, -1):
        new = [0] * n
        new[i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                new[j] = dp[j - 1] + 2      # dp here is row i+1: s[i+1..j-1]
            else:
                new[j] = max(dp[j], new[j - 1])
        dp = new
    return dp[n - 1]
