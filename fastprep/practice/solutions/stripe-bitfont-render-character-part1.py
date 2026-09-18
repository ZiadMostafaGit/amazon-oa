# Index lookup of the target character, then per-row translation of 0/1 to ./#.
from typing import List, Optional, Any


def renderCharacter(characters: str, bitmaps: List[List[str]], target: str) -> List[str]:
    idx = characters.index(target)
    table = str.maketrans({'0': '.', '1': '#'})
    return [row.translate(table) for row in bitmaps[idx]]
