# Approach: linear scan filtering out characters that are vowels.


def removeVowel(engStr: str) -> str:
    vowels = set("aeiouAEIOU")
    return "".join(ch for ch in engStr if ch not in vowels)
