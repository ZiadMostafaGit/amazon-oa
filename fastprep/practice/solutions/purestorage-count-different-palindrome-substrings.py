# Manacher's algorithm: total palindromic substring occurrences = sum of odd + even radii.


def countDifferentPalindromeSubstrings(s: str) -> int:
    n = len(s)
    if n == 0:
        return 0
    d1 = [0] * n
    l, r = 0, -1
    for i in range(n):
        k = 1 if i > r else min(d1[l + r - i], r - i + 1)
        while i - k >= 0 and i + k < n and s[i - k] == s[i + k]:
            k += 1
        d1[i] = k
        k -= 1
        if i + k > r:
            l, r = i - k, i + k
    d2 = [0] * n
    l, r = 0, -1
    for i in range(n):
        k = 0 if i > r else min(d2[l + r - i + 1], r - i + 1)
        while i - k - 1 >= 0 and i + k < n and s[i - k - 1] == s[i + k]:
            k += 1
        d2[i] = k
        k -= 1
        if i + k > r:
            l, r = i - k - 1, i + k
    return sum(d1) + sum(d2)
