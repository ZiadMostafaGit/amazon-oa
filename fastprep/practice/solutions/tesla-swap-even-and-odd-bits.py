# Bit masking: shift even-position bits up by one and odd-position bits down by one, within 32 bits.
def swapEvenOddBits(n: int) -> int:
    n &= 0xFFFFFFFF
    even = n & 0x55555555
    odd = n & 0xAAAAAAAA
    return ((even << 1) | (odd >> 1)) & 0xFFFFFFFF
