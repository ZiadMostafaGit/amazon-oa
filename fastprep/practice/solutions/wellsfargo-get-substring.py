# Slide a window over the positions of the '1's: every minimal substring starts and ends at a '1'.
def getSubstring(input_str: str, k: int) -> str:
    ones = [i for i, c in enumerate(input_str) if c == '1']
    best = None
    for i in range(len(ones) - k + 1):
        start = ones[i]
        end = ones[i + k - 1]
        cand = input_str[start:end + 1]
        if best is None or len(cand) < len(best) or (len(cand) == len(best) and cand < best):
            best = cand
    return best if best is not None else ""
