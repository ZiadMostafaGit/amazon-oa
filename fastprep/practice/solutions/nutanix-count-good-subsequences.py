# Approach: for each common frequency k, multiply (C(cnt_c, k) + 1) over letters and subtract the empty pick.
from collections import Counter


def countGoodSubsequences(word: str) -> int:
    MOD = 10 ** 9 + 7
    counts = [c for c in Counter(word).values()]
    if not counts:
        return 0
    n = max(counts)

    # factorials up to the largest letter count
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD
    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    def comb(a: int, b: int) -> int:
        if b < 0 or b > a:
            return 0
        return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD

    total = 0
    for k in range(1, n + 1):
        prod = 1
        for c in counts:
            if c >= k:
                prod = prod * (comb(c, k) + 1) % MOD
        # subtract the single way of choosing no letter at all
        total = (total + prod - 1) % MOD
    return total % MOD
