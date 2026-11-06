def getMinOperations(n: int) -> int:
    # Greedy on bits: a lone 1-bit costs one subtraction; a run of 1-bits is
    # cheaper to round up (add the lowest bit), which carries into one bit.
    ops = 0
    while n:
        if n & 1:
            ops += 1
            if n & 3 == 3:
                n += 1
            else:
                n -= 1
        n >>= 1
    return ops
