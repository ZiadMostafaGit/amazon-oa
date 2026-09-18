# Kept characters must form a prefix of reverse(s); moved ones can be appended in any order,
# so the answer is n minus the longest prefix of reverse(s) that is a subsequence of s.
def reverseBinaryString(s: str) -> int:
    n = len(s)
    t = s[::-1]
    j = 0
    for ch in s:
        if j < n and t[j] == ch:
            j += 1
    return n - j
