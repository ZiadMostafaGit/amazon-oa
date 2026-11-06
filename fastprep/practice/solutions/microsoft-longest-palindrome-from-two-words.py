# Longest palindromic subsequence of word1 + word2, but only counting pairs (i, j) with
# i in word1 and j in word2 as the outermost match, so both words contribute.
def maxPalindromeFromTwoWords(word1: str, word2: str) -> int:
    s = word1 + word2
    n, a = len(s), len(word1)
    best = 0
    dp = [0] * n                       # row i+1 of dp[i][j] = LPS of s[i..j]
    for i in range(n - 1, -1, -1):
        new = [0] * n
        new[i] = 1
        si = s[i]
        for j in range(i + 1, n):
            if si == s[j]:
                new[j] = dp[j - 1] + 2
                if i < a <= j and new[j] > best:
                    best = new[j]
            else:
                new[j] = dp[j] if dp[j] > new[j - 1] else new[j - 1]
        dp = new
    return best
