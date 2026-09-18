# Hand-written recursive-descent scan over the compact JSON that returns the raw substring span.
class _Found(Exception):
    def __init__(self, value: str):
        self.value = value


def findNestedJsonValue(json: str, targetKey: str) -> str:
    s = json
    n = len(s)

    def scan_string(i: int) -> int:
        # s[i] == '"'; returns index just past the closing quote
        j = i + 1
        while j < n and s[j] != '"':
            j += 1
        return j + 1

    def scan_value(i: int) -> int:
        c = s[i]
        if c == '"':
            return scan_string(i)
        if c == '{':
            j = i + 1
            if j < n and s[j] == '}':
                return j + 1
            while True:
                j = scan_string(j)      # key
                j += 1                  # ':'
                j = scan_value(j)       # value
                if s[j] == ',':
                    j += 1
                    continue
                return j + 1            # '}'
        if c == '[':
            j = i + 1
            if j < n and s[j] == ']':
                return j + 1
            while True:
                j = scan_value(j)
                if s[j] == ',':
                    j += 1
                    continue
                return j + 1            # ']'
        # any other literal (number / true / false / null)
        j = i
        while j < n and s[j] not in ',}]':
            j += 1
        return j

    def search_value(i: int) -> int:
        c = s[i]
        if c == '{':
            j = i + 1
            if j < n and s[j] == '}':
                return j + 1
            while True:
                kstart = j
                kend = scan_string(j)
                key = s[kstart + 1:kend - 1]
                vstart = kend + 1  # skip ':'
                if key == targetKey:
                    raise _Found(s[vstart:scan_value(vstart)])
                j = search_value(vstart)
                if s[j] == ',':
                    j += 1
                    continue
                return j + 1
        if c == '[':
            j = i + 1
            if j < n and s[j] == ']':
                return j + 1
            while True:
                j = search_value(j)
                if s[j] == ',':
                    j += 1
                    continue
                return j + 1
        return scan_value(i)

    try:
        search_value(0)
    except _Found as f:
        return f.value
    return "NOT_FOUND"
