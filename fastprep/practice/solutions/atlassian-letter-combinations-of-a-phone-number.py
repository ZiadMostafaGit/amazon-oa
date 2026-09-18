# Iterative cartesian-product expansion over the keypad letters of each digit.
from typing import List

_KEYPAD = {
    "2": "abc", "3": "def", "4": "ghi", "5": "jkl",
    "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz",
}


def letterCombinations(digits: str) -> List[str]:
    if not digits:
        return []
    combos = [""]
    for ch in digits:
        letters = _KEYPAD.get(ch, "")
        combos = [prefix + letter for prefix in combos for letter in letters]
    return combos
