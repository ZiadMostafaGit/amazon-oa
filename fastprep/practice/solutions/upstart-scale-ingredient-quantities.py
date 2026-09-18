# Parse the leading integer of each string, multiply it, and re-join the remainder.
from typing import List, Optional, Any


def scaleIngredients(ingredients: List[str], people: int) -> List[str]:
    out = []
    for item in ingredients:
        i = 0
        n = len(item)
        while i < n and item[i].isspace():
            i += 1
        start = i
        if i < n and item[i] in "+-":
            i += 1
        while i < n and item[i].isdigit():
            i += 1
        if i == start or not item[start:i].lstrip("+-"):
            out.append(item)
            continue
        qty = int(item[start:i]) * people
        out.append(item[:start] + str(qty) + item[i:])
    return out
