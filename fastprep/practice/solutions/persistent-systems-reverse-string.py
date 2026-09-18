# Approach: slice the string with a negative step to reverse it in O(n).
def reverseString(s: str) -> str:
    return s[::-1]
