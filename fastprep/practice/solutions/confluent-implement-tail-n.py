# Reverse scan from the end of the buffer, collecting at most n line boundaries (no full split).
from typing import List, Optional, Any


def tailLastNLines(n: int, fileContents: str) -> List[str]:
    if n <= 0 or not fileContents:
        return []
    end = len(fileContents)
    if fileContents.endswith("\n"):
        end -= 1          # a trailing newline terminates the last line, it does not start a new one
    if end <= 0:
        return []
    lines = []
    stop = end
    while stop > 0 and len(lines) < n:
        idx = fileContents.rfind("\n", 0, stop)
        lines.append(fileContents[idx + 1:stop])
        stop = idx
        if idx == -1:
            break
    lines.reverse()
    return lines
