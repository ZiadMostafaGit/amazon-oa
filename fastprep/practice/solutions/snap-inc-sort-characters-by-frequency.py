# Counting sort by (-frequency, ascii) then rebuild the string.
from collections import Counter


def frequencySort(s: str) -> str:
    freq = Counter(s)
    order = sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))
    return "".join(ch * cnt for ch, cnt in order)
