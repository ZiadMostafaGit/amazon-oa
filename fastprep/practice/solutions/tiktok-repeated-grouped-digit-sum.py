# Direct simulation: chunk the string into groups of k, replace each group with its digit sum, repeat.
def repeatedGroupedDigitSum(number: str, k: int) -> str:
    while len(number) > k:
        parts = []
        for i in range(0, len(number), k):
            group = number[i:i + k]
            parts.append(str(sum(ord(c) - 48 for c in group)))
        number = "".join(parts)
    return number
