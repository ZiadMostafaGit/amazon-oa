# Single linear scan implementing the restricted grammar: optional '-', digits, at most one '.' with digits on both sides.
def isNumber(toTest: str) -> bool:
    if not toTest:
        return False

    i = 0
    n = len(toTest)
    if toTest[0] == '-':
        i = 1

    digits_before = 0
    while i < n and '0' <= toTest[i] <= '9':
        digits_before += 1
        i += 1
    if digits_before == 0:
        return False

    if i == n:
        return True

    if toTest[i] != '.':
        return False
    i += 1

    digits_after = 0
    while i < n and '0' <= toTest[i] <= '9':
        digits_after += 1
        i += 1

    return digits_after > 0 and i == n
