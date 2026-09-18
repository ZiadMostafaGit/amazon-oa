# KMP failure function: the last prefix-function value is the longest happy prefix.
def solve(s: str) -> str:
    n = len(s)
    if n < 2:
        return ""
    failure = [0] * n
    length = 0
    for i in range(1, n):
        while length and s[i] != s[length]:
            length = failure[length - 1]
        if s[i] == s[length]:
            length += 1
        failure[i] = length
    return s[:failure[-1]]
