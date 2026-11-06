# Count letters of s up, letters of t down; anagrams iff every count returns to zero. O(n).
def isAnagram(s: str, t: str) -> bool:
    if len(s) != len(t):
        return False
    count = [0] * 26
    for ch in s:
        count[ord(ch) - 97] += 1
    for ch in t:
        k = ord(ch) - 97
        count[k] -= 1
        if count[k] < 0:
            return False
    return True
