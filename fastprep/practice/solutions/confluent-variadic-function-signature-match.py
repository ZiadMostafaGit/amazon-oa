# Direct signature check per function: exact positional match, or fixed prefix plus a repeated final type.
from typing import List, Optional, Any


def findMatchingFunctions(functionNames: List[str], functionArgumentTypes: List[List[str]], isVariadic: List[bool], callArgumentTypes: List[str]) -> List[str]:
    n = len(callArgumentTypes)
    result: List[str] = []
    for i, name in enumerate(functionNames):
        declared = functionArgumentTypes[i]
        m = len(declared)
        variadic = bool(isVariadic[i]) if i < len(isVariadic) else False
        if variadic:
            if m == 0 or n < m:
                continue
            ok = True
            for k in range(m - 1):
                if declared[k] != callArgumentTypes[k]:
                    ok = False
                    break
            if ok:
                last = declared[m - 1]
                for k in range(m - 1, n):
                    if callArgumentTypes[k] != last:
                        ok = False
                        break
            if ok:
                result.append(name)
        else:
            if m == n and all(declared[k] == callArgumentTypes[k] for k in range(n)):
                result.append(name)
    return result
