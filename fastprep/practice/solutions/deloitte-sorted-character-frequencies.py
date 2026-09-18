# Counting sort over the 26 lowercase letters, then concatenate char + count in order.
from collections import Counter


def sortedCharacterFrequencies(word: str) -> str:
    counts = Counter(word)
    return "".join(ch + str(counts[ch]) for ch in sorted(counts))
