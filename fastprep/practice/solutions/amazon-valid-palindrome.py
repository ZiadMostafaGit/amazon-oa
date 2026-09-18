# Two pointers skipping non-alphanumeric characters, comparing case-folded.
def isValidPalindrome(s: str) -> bool:
    i, j = 0, len(s) - 1
    while i < j:
        while i < j and not s[i].isalnum():
            i += 1
        while i < j and not s[j].isalnum():
            j -= 1
        if i < j:
            a, b = s[i], s[j]
            if ('a' <= a <= 'z' or 'A' <= a <= 'Z'):
                a = a.lower()
            if ('a' <= b <= 'z' or 'A' <= b <= 'Z'):
                b = b.lower()
            if a != b:
                return False
            i += 1
            j -= 1
    return True
