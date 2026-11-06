# Grid paths: ways[r][c] = ways from above + ways from the left, kept as one rolling row.
def uniquePaths(m: int, n: int) -> int:
    row = [1] * n
    for _ in range(1, m):
        for c in range(1, n):
            row[c] += row[c - 1]
    return row[-1]
