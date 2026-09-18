# Prefix-XOR identity: since 4 | n the range XOR equals xor(0..x), maximized at x = 2^bits - 2.
def getMaxX(n: int) -> int:
    bits = n.bit_length()
    best_v = -1
    best_x = n
    # xor(0..x) pattern by x % 4: x, 1, x+1, 0
    def prefix(x: int) -> int:
        r = x % 4
        if r == 0:
            return x
        if r == 1:
            return 1
        if r == 2:
            return x + 1
        return 0

    low = n
    high = (1 << bits) - 1
    # Candidates that can maximize prefix(x): the largest x==0 mod 4 and the largest x==2 mod 4
    cands = set()
    for r in (0, 2):
        x = high - ((high - r) % 4)
        if x >= low:
            cands.add(x)
    cands.add(low)
    for x in sorted(cands):
        v = prefix(x)
        if v > best_v:
            best_v = v
            best_x = x
    return best_x
