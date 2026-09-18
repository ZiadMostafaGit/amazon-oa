# Frequency count, then a second pass to find the first character with count one.
from collections import Counter


def firstNonRepeatingCharacter(text: str) -> str:
    counts = Counter(text)
    for ch in text:
        if counts[ch] == 1:
            return ch
    return ""
