import json
from typing import List


class NestedIterator:
    def __init__(self, nested):
        self.stack = [(nested, 0)]  # (list, next index)

    def _settle(self):
        # Advance until the top of the stack points at an integer, or empty.
        while self.stack:
            lst, i = self.stack[-1]
            if i >= len(lst):
                self.stack.pop()
                continue
            x = lst[i]
            if isinstance(x, list):
                self.stack[-1] = (lst, i + 1)
                self.stack.append((x, 0))
            else:
                return True
        return False

    def hasNext(self):
        return self._settle()

    def next(self):
        self._settle()
        lst, i = self.stack[-1]
        self.stack[-1] = (lst, i + 1)
        return lst[i]


def runNestedIterator(nestedList: str, operations: List[str]) -> List[str]:
    it = NestedIterator(json.loads(nestedList))
    out = []
    for op in operations:
        if op == "HAS_NEXT":
            out.append("true" if it.hasNext() else "false")
        else:
            out.append(str(it.next()))
    return out
