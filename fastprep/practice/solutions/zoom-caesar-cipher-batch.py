# Per-operation character mapping with a shift reduced modulo 26, applied within each letter case.
from typing import List, Optional, Any


def caesarCipher(actions: List[str], texts: List[str], shifts: List[int]) -> List[str]:
    results = []
    for action, text, shift in zip(actions, texts, shifts):
        step = shift % 26
        if action == "decrypt":
            step = (26 - step) % 26
        if step == 0:
            results.append(text)
            continue
        out = []
        for ch in text:
            code = ord(ch)
            if 97 <= code <= 122:
                out.append(chr(97 + (code - 97 + step) % 26))
            elif 65 <= code <= 90:
                out.append(chr(65 + (code - 65 + step) % 26))
            else:
                out.append(ch)
        results.append("".join(out))
    return results
