# Classic Levenshtein dynamic programming over a rolling row.
def editDistance(source: str, target: str) -> int:
    n, m = len(source), len(target)
    prev = list(range(m + 1))
    for i in range(1, n + 1):
        cur = [i] + [0] * m
        si = source[i - 1]
        for j in range(1, m + 1):
            if si == target[j - 1]:
                cur[j] = prev[j - 1]
            else:
                cur[j] = 1 + min(prev[j - 1], prev[j], cur[j - 1])
        prev = cur
    return prev[m]
