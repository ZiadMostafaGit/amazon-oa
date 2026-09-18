# Direct simulation: concatenate per-row glyph slices, zero-padding short glyphs.
from typing import List


def renderWord(text: str, characters: str, bitmaps: List[List[str]]) -> List[str]:
    if not text:
        return []
    index = {ch: i for i, ch in enumerate(characters)}
    glyphs = [bitmaps[index[ch]] for ch in text]
    height = len(glyphs[0])
    out = []
    for r in range(height):
        parts = []
        for g in glyphs:
            if r < len(g):
                parts.append(g[r])
            else:
                parts.append("0" * len(g[0]))
        out.append("".join(parts).replace("0", ".").replace("1", "#"))
    return out
