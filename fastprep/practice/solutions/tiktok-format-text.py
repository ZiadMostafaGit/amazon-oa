# Greedy word wrapping per paragraph, pad to width by alignment, then wrap in a '*' border.
from typing import List, Optional, Any


def formatText(paragraphs: List[str], alignments: List[str], width: int) -> List[str]:
    lines: List[str] = []
    for i, para in enumerate(paragraphs):
        align = alignments[i] if i < len(alignments) else "LEFT"
        words = para.split()
        j = 0
        n = len(words)
        while j < n:
            cur = words[j]
            j += 1
            while j < n and len(cur) + 1 + len(words[j]) <= width:
                cur += " " + words[j]
                j += 1
            pad = width - len(cur)
            if pad < 0:
                pad = 0
            if align == "RIGHT":
                lines.append(" " * pad + cur)
            else:
                lines.append(cur + " " * pad)
    border = "*" * (width + 2)
    out = [border]
    for line in lines:
        out.append("*" + line + "*")
    out.append(border)
    return out
