# Greedy line packing per paragraph, then pad each line to the fixed width on the side the alignment requires.
from typing import List, Optional, Any


def formatNewspaperPage(paragraphs: List[List[str]], aligns: List[str], width: int) -> List[str]:
    out = []
    for idx, words in enumerate(paragraphs):
        align = aligns[idx] if idx < len(aligns) else "LEFT"
        line = []
        length = 0
        for w in words:
            need = len(w) if not line else length + 1 + len(w)
            if line and need > width:
                out.append(_pad(" ".join(line), width, align))
                line = [w]
                length = len(w)
            else:
                line.append(w)
                length = need
        if line:
            out.append(_pad(" ".join(line), width, align))
    return out


def _pad(text: str, width: int, align: str) -> str:
    fill = " " * (width - len(text))
    return fill + text if align == "RIGHT" else text + fill
