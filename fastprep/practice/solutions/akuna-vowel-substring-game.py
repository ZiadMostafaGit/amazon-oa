# Game theory: Alex can take the whole odd-vowel part on move one, so he wins iff the string has any vowel.
from typing import List, Optional, Any

VOWELS = frozenset("aeiou")


def determineWinners(datasets: List[str]) -> List[str]:
    res = []
    for s in datasets:
        has_vowel = False
        for ch in s:
            if ch in VOWELS:
                has_vowel = True
                break
        res.append("Alex" if has_vowel else "Chris")
    return res
