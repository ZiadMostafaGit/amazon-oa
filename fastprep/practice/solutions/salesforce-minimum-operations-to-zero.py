# Non-adjacent form (NAF) signed-binary greedy: minimum weight signed power-of-two representation.
def getMinOperations(n: int) -> int:
    ops = 0
    while n:
        if n & 1:
            # 0b11 tail -> adding 1 clears a longer run than subtracting 1
            if (n & 3) == 3:
                n += 1
            else:
                n -= 1
            ops += 1
        else:
            n >>= 1
    return ops
