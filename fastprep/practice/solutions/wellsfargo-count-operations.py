# The permutation's order = lcm of its cycle lengths; combine prime powers with a
# smallest-prime-factor sieve so the lcm can be reduced modulo 1e9+7.
from typing import List, Optional, Any

MOD = 10 ** 9 + 7


def countOperations(p: List[int]) -> int:
    n = len(p)
    if n == 0:
        return 1

    # Smallest prime factor sieve up to n.
    spf = list(range(n + 1))
    i = 2
    while i * i <= n:
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
        i += 1

    seen = [False] * (n + 1)
    max_exp = {}
    for start in range(1, n + 1):
        if seen[start]:
            continue
        length = 0
        node = start
        while not seen[node]:
            seen[node] = True
            node = p[node - 1]
            length += 1
        # Factor the cycle length, keeping the largest exponent per prime.
        m = length
        while m > 1:
            prime = spf[m]
            exp = 0
            while m % prime == 0:
                m //= prime
                exp += 1
            if exp > max_exp.get(prime, 0):
                max_exp[prime] = exp

    answer = 1
    for prime, exp in max_exp.items():
        answer = (answer * pow(prime, exp, MOD)) % MOD
    return answer
