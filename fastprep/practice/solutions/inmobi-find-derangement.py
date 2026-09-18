# Linear DP recurrence D(n) = (n-1) * (D(n-1) + D(n-2)) modulo 1e9+7.
def findDerangement(n: int) -> int:
    MOD = 10 ** 9 + 7
    if n == 0:
        return 1
    if n == 1:
        return 0
    prev2, prev1 = 1, 0  # D(0), D(1)
    for i in range(2, n + 1):
        cur = (i - 1) * (prev1 + prev2) % MOD
        prev2, prev1 = prev1, cur
    return prev1
