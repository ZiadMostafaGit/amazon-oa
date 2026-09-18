# Direct string formatting: parse header, then emit interleaved border and padded rows.
from typing import List, Optional, Any


def solvePrintSentencesAsTable(input: str) -> List[str]:
    lines = input.split("\n")
    if not lines or not lines[0].strip():
        return []
    parts = lines[0].split()
    n = int(parts[0])
    width = int(parts[1])
    if n == 0:
        return []
    border = "+" + "-" * (width + 2) + "+"
    out = []
    for i in range(1, n + 1):
        sentence = lines[i] if i < len(lines) else ""
        sentence = sentence.rstrip("\r")
        out.append(border)
        out.append("| " + sentence + " " * (width - len(sentence)) + " |")
    out.append(border)
    return out
