# Hash map from source path to encoded value, then one lookup per target field.
from typing import List, Optional, Any


def projectJsonFields(sourceFields: List[List[str]], targetFields: List[List[str]]) -> List[List[str]]:
    lookup = {}
    for row in sourceFields:
        lookup[row[0]] = row[1]
    out = []
    for row in targetFields:
        out.append([row[0], lookup.get(row[1], "null")])
    return out
