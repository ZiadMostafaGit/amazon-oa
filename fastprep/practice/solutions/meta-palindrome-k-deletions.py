# Longest palindromic subsequence DP: answer is len(s) - LPS(s) <= k.


def isValidPalindrome(s: str, k: int) -> bool:
    n = len(s)
    if n <= 1:
        return True
    # dp[j] over increasing lengths; dp[i][j] = LPS of s[i..j]
    prev = [0] * n
    cur = [0] * n
    for i in range(n - 1, -1, -1):
        cur = [0] * n
        cur[i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                cur[j] = (prev[j - 1] if j - 1 >= i + 1 else 0) + 2
                if j == i + 1:
                    cur[j] = 2
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur
    return n - prev[n - 1] <= k
