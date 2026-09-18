# Expand around each center; keep longest palindrome of length >= 2, breaking ties lexicographically.
def findPalindromeSubString(inputStr: str) -> str:
    s = inputStr or ""
    n = len(s)
    best = ""

    def consider(lo: int, hi: int) -> None:
        nonlocal best
        while lo >= 0 and hi < n and s[lo] == s[hi]:
            length = hi - lo + 1
            if length > 1:
                cand = s[lo:hi + 1]
                if len(cand) > len(best) or (len(cand) == len(best) and cand < best):
                    best = cand
            lo -= 1
            hi += 1

    for i in range(n):
        consider(i, i)
        consider(i, i + 1)
    return best if best else "None"
