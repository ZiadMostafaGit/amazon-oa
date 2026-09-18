# Reverse the digits, then greedily split: a leading '1' means a 3-digit code, otherwise 2 digits.
def decodingString(encode: str) -> str:
    s = encode[::-1]
    n = len(s)
    out = []
    i = 0
    while i < n:
        take = 3 if s[i] == '1' else 2
        code = int(s[i:i + take])
        out.append(chr(code))
        i += take
    return ''.join(out)
