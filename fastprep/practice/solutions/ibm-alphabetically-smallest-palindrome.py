# Counting: fix parity by moving one unit from the largest odd letters to the smallest odd letters.
def makeAlphabeticallySmallestPalindrome(s: str) -> str:
    count = [0] * 26
    for ch in s:
        count[ord(ch) - 97] += 1
    odds = [i for i in range(26) if count[i] % 2 == 1]
    m = len(odds)
    k = m // 2
    # the k smallest odd letters each receive one unit, taken from the k largest odd letters
    for t in range(k):
        recv = odds[t]
        donor = odds[m - 1 - t]
        count[recv] += 1
        count[donor] -= 1
    middle = ''
    if m % 2 == 1:
        middle = chr(97 + odds[k])
    half = ''.join(chr(97 + i) * (count[i] // 2) for i in range(26))
    return half + middle + half[::-1]
