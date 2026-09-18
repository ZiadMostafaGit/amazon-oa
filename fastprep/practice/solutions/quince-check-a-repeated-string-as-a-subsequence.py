# Length check prunes impossible cases, then a single greedy two-pointer subsequence scan.
def isRepeatedSubsequence(str1: str, str2: str, k: int) -> bool:
    n = len(str1)
    m = len(str2)
    if m * k > n:
        return False
    i = 0
    for _ in range(k):
        for ch in str2:
            while i < n and str1[i] != ch:
                i += 1
            if i >= n:
                return False
            i += 1
    return True
