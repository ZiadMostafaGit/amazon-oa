# Group the absolute value's digits in threes from the right, then reattach the sign.
def formatWithCommas(value: int) -> str:
    sign = "-" if value < 0 else ""
    digits = str(abs(value))
    groups = []
    i = len(digits)
    while i > 3:
        groups.append(digits[i - 3:i])
        i -= 3
    groups.append(digits[:i])
    return sign + ",".join(reversed(groups))
