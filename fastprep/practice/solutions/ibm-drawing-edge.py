# Each of the n*(n-1)/2 vertex pairs is independently present or absent: 2^(n*(n-1)/2) mod 1e9+7.
MOD = 10 ** 9 + 7


def drawingEdge(n: int) -> int:
    edges = n * (n - 1) // 2
    return pow(2, edges, MOD)
