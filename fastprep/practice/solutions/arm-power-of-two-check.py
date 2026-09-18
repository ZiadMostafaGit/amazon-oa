# Bit trick: a positive power of two has exactly one set bit, so n & (n - 1) == 0.
def isPowerOfTwo(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0
