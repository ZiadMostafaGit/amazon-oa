# Greedy line packing with a header stack: each new chunk is prefixed by the active header path.
from typing import List, Optional, Any

SEP = " | "


def _header_level(line: str) -> int:
    stripped = line.lstrip()
    if not stripped.startswith("#"):
        return 0
    level = 0
    for ch in stripped:
        if ch == "#":
            level += 1
        else:
            break
    return level


def _display_len(lines: List[str]) -> int:
    if not lines:
        return 0
    return sum(len(x) for x in lines) + len(SEP) * (len(lines) - 1)


def chunkMarkdown(markdown: str, maxChunkSize: int) -> List[str]:
    if markdown is None or markdown == "":
        return []
    lines = markdown.split("\n")

    chunks: List[List[str]] = []
    current: List[str] = []
    stack: List[tuple] = []  # (level, text)

    for line in lines:
        level = _header_level(line)
        if level > 0:
            while stack and stack[-1][0] >= level:
                stack.pop()
            path = [h[1] for h in stack]
            stack.append((level, line))
        else:
            path = [h[1] for h in stack]

        if not current:
            current = path + [line]
            continue

        if _display_len(current) + len(SEP) + len(line) <= maxChunkSize:
            current.append(line)
        else:
            chunks.append(current)
            current = path + [line]

    if current:
        chunks.append(current)

    return [SEP.join(c) for c in chunks]
