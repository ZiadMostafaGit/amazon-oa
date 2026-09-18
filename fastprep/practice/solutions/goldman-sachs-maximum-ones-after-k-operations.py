# Greedy counting: every zero that has a '1' somewhere to its right can be flipped by one operation.
def maximumOnes(s: str, k: int) -> int:
    ones = 0
    convertible = 0
    seen_one_to_right = False
    for ch in reversed(s):
        if ch == '1':
            ones += 1
            seen_one_to_right = True
        else:
            if seen_one_to_right:
                convertible += 1
    return ones + min(k, convertible)
