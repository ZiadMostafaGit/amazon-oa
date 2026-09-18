# Character-frequency comparison after lowercasing both words.
from collections import Counter


def isAnagram(wordA: str, wordB: str) -> bool:
    if len(wordA) != len(wordB):
        return False
    return Counter(wordA.lower()) == Counter(wordB.lower())
