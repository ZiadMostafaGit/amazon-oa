# Greedy over bits: equal bits become 1 in both numbers, differing bits are split high-to-low to balance the factors.
def xorMultiplication(A: int, B: int, N: int) -> int:
    MOD = 10 ** 9 + 7
    common = 0          # bits where A and B agree -> X can make both 1
    diff_bits = []      # bits where they differ -> exactly one factor gets it
    for i in range(N):
        a = (A >> i) & 1
        b = (B >> i) & 1
        if a == b:
            common |= 1 << i
        else:
            diff_bits.append(i)

    u = common
    v = common
    for i in reversed(diff_bits):   # highest differing bit first
        if u <= v:
            u += 1 << i
        else:
            v += 1 << i

    return (u % MOD) * (v % MOD) % MOD
