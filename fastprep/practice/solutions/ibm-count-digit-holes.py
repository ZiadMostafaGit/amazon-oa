# Digit lookup table summing holes per digit.
def countDigitHoles(number: int) -> int:
    holes = {'0': 1, '4': 1, '6': 1, '9': 1, '8': 2}
    return sum(holes.get(c, 0) for c in str(number))
