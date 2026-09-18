# Counting: each of the n*(n-1)/2 unordered pairs is independently present or absent -> 2^C(n,2) mod 1e9+7.
def drawingEdge(n: int) -> int:
    MOD = 10**9 + 7
    pairs = n * (n - 1) // 2
    return pow(2, pairs, MOD)
