# Direct keypad lookup table, emitting a '#' separator when consecutive letters share a key.
KEYS = {
    '2': "abc", '3': "def", '4': "ghi", '5': "jkl",
    '6': "mno", '7': "pqrs", '8': "tuv", '9': "wxyz",
}
CODE = {}
for _digit, _letters in KEYS.items():
    for _i, _ch in enumerate(_letters):
        CODE[_ch] = _digit * (_i + 1)


def encodeKeypad(text: str) -> str:
    out = []
    prev_key = ''
    for ch in text:
        low = ch.lower()
        seq = CODE.get(low)
        if seq is None:
            continue
        key = seq[0]
        if prev_key == key:
            out.append('#')
        out.append(seq)
        prev_key = key
    return ''.join(out)
