# Counting: cycle W, D, L round-robin, emitting each character while its count remains.
def reorderWdl(sequence: str) -> str:
    counts = {'W': 0, 'D': 0, 'L': 0}
    for ch in sequence:
        if ch in counts:
            counts[ch] += 1
    out = []
    remaining = counts['W'] + counts['D'] + counts['L']
    while remaining > 0:
        for ch in ('W', 'D', 'L'):
            if counts[ch] > 0:
                counts[ch] -= 1
                remaining -= 1
                out.append(ch)
    return ''.join(out)
