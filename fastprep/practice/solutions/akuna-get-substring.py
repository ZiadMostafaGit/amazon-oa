# Collect the '1' positions, slide a window of k ones, keep the shortest then lexicographically smallest span.
def getSubstring(input_str: str, k: int) -> str:
    ones = [i for i, ch in enumerate(input_str) if ch == '1']
    best = None
    for i in range(len(ones) - k + 1):
        cand = input_str[ones[i]:ones[i + k - 1] + 1]
        if best is None or len(cand) < len(best) or (len(cand) == len(best) and cand < best):
            best = cand
    return best if best is not None else ""
