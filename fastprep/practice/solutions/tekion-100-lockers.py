# A locker ends open iff its number has an odd divisor count, i.e. it is a perfect square: answer is isqrt(n).
import math


def openLockers(n: int) -> int:
    return math.isqrt(n)
