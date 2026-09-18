# Expand around each of the 2n-1 centers and count every palindromic occurrence.
def countPalindromicSubstrings(s: str) -> int:
    n = len(s)
    total = 0
    for center in range(2 * n - 1):
        left = center // 2
        right = left + (center & 1)
        while left >= 0 and right < n and s[left] == s[right]:
            total += 1
            left -= 1
            right += 1
    return total
