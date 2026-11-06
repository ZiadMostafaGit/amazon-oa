# Count occurrences of a pattern as a subsequence: ways[j] = ways to match pattern[:j] in the text so far.
def getSubsequenceCount(s1: str, s2: str) -> int:
    m = len(s1)
    ways = [1] + [0] * m
    for ch in s2:
        for j in range(m, 0, -1):          # downward: one text character fills one pattern slot
            if s1[j - 1] == ch:
                ways[j] += ways[j - 1]
    return ways[m]
