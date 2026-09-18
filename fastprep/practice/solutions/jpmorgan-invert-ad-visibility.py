# XOR with the all-ones mask spanning the value's significant bit width.


def invertAdVisibility(base10: int) -> int:
    if base10 <= 0:
        return 0
    return base10 ^ ((1 << base10.bit_length()) - 1)
