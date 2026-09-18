# Single linear scan tokenizing letter+digits pairs into a 26-slot accumulator.
def aggregateLetterValues(encoded: str) -> str:
    totals = [0] * 26
    seen = [False] * 26
    n = len(encoded)
    i = 0
    while i < n:
        idx = ord(encoded[i]) - 65
        i += 1
        start = i
        while i < n and encoded[i].isdigit():
            i += 1
        if start == i:
            continue
        seen[idx] = True
        totals[idx] += int(encoded[start:i])
    parts = []
    for k in range(26):
        if seen[k]:
            parts.append(chr(65 + k))
            parts.append(str(totals[k]))
    return "".join(parts)
