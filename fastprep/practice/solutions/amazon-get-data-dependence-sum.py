# Divisor-block enumeration: every distinct value of floor(n/k) visited once in O(sqrt(n)).


def getDataDependenceSum(n: int) -> int:
    if n <= 0:
        return 0
    total = 0          # k > n contributes the value 0, which adds nothing
    k = 1
    while k <= n:
        v = n // k
        total += v
        k = n // v + 1
    return total
