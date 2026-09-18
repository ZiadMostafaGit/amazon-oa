# Greedy line wrapping per paragraph, then pad each line left/right and add a '*' border.
from typing import List, Optional, Any


def formatNewspaperPage(paragraphs: List[List[str]], aligns: List[str], width: int) -> List[str]:
    wrapped = []  # (line_text, align)
    for idx, para in enumerate(paragraphs):
        align = aligns[idx] if idx < len(aligns) else "LEFT"
        cur = None
        for word in para:
            if cur is None:
                cur = word
            elif len(cur) + 1 + len(word) <= width:
                cur = cur + " " + word
            else:
                wrapped.append((cur, align))
                cur = word
        if cur is not None:
            wrapped.append((cur, align))

    border = "*" * (width + 2)
    out = [border]
    for text, align in wrapped:
        if align == "RIGHT":
            padded = text.rjust(width)
        else:
            padded = text.ljust(width)
        out.append("*" + padded + "*")
    out.append(border)
    return out
