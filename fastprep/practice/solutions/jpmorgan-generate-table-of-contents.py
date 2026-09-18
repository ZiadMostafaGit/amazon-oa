# Single pass over the lines, tracking chapter and section counters.
from typing import List


def generateTableOfContents(text: List[str]) -> List[str]:
    toc: List[str] = []
    chapter = 0
    section = 0
    for line in text:
        if line.startswith("## "):
            if chapter == 0:
                continue
            section += 1
            toc.append("%d.%d. %s" % (chapter, section, line[3:].strip()))
        elif line.startswith("# "):
            chapter += 1
            section = 0
            toc.append("%d. %s" % (chapter, line[2:].strip()))
    return toc
