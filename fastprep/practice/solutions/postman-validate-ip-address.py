# Split-and-validate each segment against the IPv4 and IPv6 grammar rules.
def validIPAddress(queryIP: str) -> str:
    if queryIP.count('.') == 3 and ':' not in queryIP:
        parts = queryIP.split('.')
        if len(parts) != 4:
            return "Neither"
        for p in parts:
            if not p or len(p) > 3:
                return "Neither"
            if not all('0' <= c <= '9' for c in p):
                return "Neither"
            if len(p) > 1 and p[0] == '0':
                return "Neither"
            if int(p) > 255:
                return "Neither"
        return "IPv4"
    if queryIP.count(':') == 7 and '.' not in queryIP:
        groups = queryIP.split(':')
        if len(groups) != 8:
            return "Neither"
        hexd = set("0123456789abcdefABCDEF")
        for g in groups:
            if not g or len(g) > 4:
                return "Neither"
            for c in g:
                if c not in hexd:
                    return "Neither"
        return "IPv6"
    return "Neither"
