# Direct string formatting: chunk bytes into rows, build offset / hex slots / ascii column.
from typing import List, Optional, Any


def formatHexDump(bytes: List[int], bytesPerRow: int) -> List[str]:
    rows = []
    n = len(bytes)
    for start in range(0, n, bytesPerRow):
        chunk = bytes[start:start + bytesPerRow]
        offset = "%08x" % start
        slots = ["%02X" % b for b in chunk]
        while len(slots) < bytesPerRow:
            slots.append("  ")
        hex_part = " ".join(slots)
        ascii_part = "".join(chr(b) if 0x20 <= b <= 0x7E else "." for b in chunk)
        rows.append(offset + "  " + hex_part + "  |" + ascii_part + "|")
    return rows
