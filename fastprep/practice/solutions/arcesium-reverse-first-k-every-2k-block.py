# Walk the string in strides of 2k and reverse the first k characters of each stride.
def reverseFirstKInEvery2KBlock(s: str, k: int) -> str:
    chars = list(s)
    n = len(chars)
    for start in range(0, n, 2 * k):
        end = min(start + k, n)
        chars[start:end] = reversed(chars[start:end])
    return "".join(chars)
