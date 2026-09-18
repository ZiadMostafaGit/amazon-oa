# Linear DP with the classic recurrence f(n) = 2*f(n-1) + f(n-3).
def numTilings(n: int) -> int:
    MOD = 10 ** 9 + 7
    if n <= 2:
        return n
    f = [0] * (n + 1)
    f[0], f[1], f[2] = 1, 1, 2
    for i in range(3, n + 1):
        f[i] = (2 * f[i - 1] + f[i - 3]) % MOD
    return f[n]
