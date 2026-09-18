# The answer is the maximum suffix; computed with the linear Duval-style scan.
def alphabeticallyMaximumSubstring(s: str) -> str:
    n = len(s)
    i, j, k = 0, 1, 0
    while j + k < n:
        a = s[i + k]
        b = s[j + k]
        if a == b:
            k += 1
        elif a < b:
            i = max(i + k + 1, j)
            j = i + 1
            k = 0
        else:
            j = j + k + 1
            k = 0
    return s[i:]
