# Counting: repeatedly emit W, D, L while any remain.
from collections import Counter


def constructWdlString(inputStr: str) -> str:
    counts = Counter(inputStr)
    out = []
    while counts['W'] or counts['D'] or counts['L']:
        for ch in 'WDL':
            if counts[ch] > 0:
                counts[ch] -= 1
                out.append(ch)
    return ''.join(out)
