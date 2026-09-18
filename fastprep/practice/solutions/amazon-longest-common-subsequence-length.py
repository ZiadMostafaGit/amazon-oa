# Classic LCS dynamic programming with a rolling 1-D row (O(n*m) time, O(min) space).
def solve(first: str, second: str) -> int:
    if not first or not second:
        return 0
    if len(second) > len(first):
        first, second = second, first
    m = len(second)
    prev = [0] * (m + 1)
    for ch in first:
        cur = [0] * (m + 1)
        for j in range(1, m + 1):
            if ch == second[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = cur[j - 1] if cur[j - 1] >= prev[j] else prev[j]
        prev = cur
    return prev[m]
