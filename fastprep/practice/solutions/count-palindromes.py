# Expand around each of the 2n-1 centers, counting every palindromic substring.
def countPalindromes(s: str) -> int:
    n = len(s)
    total = 0
    for center in range(2 * n - 1):
        lo = center // 2
        hi = lo + (center & 1)
        while lo >= 0 and hi < n and s[lo] == s[hi]:
            total += 1
            lo -= 1
            hi += 1
    return total
