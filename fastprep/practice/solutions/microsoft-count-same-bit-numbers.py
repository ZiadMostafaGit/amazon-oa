# Combinatorics: f(n) is the all-ones number of the same bit length, so the answer is C(bits, popcount) - 1.
from math import comb


def countSameBitNumbers(n: int) -> int:
    MOD = 1_000_000_007
    b = n.bit_length()
    k = bin(n).count("1")
    return (comb(b, k) - 1) % MOD
