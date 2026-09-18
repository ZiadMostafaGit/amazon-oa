# Two hash maps (url -> token, token -> url) with a counter encoded in Base62.
from typing import List, Optional, Any

_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _encode(num: int) -> str:
    if num == 0:
        return _ALPHABET[0]
    out = []
    while num > 0:
        num, rem = divmod(num, 62)
        out.append(_ALPHABET[rem])
    out.reverse()
    return "".join(out)


def runUrlShortener(operations: List[str], values: List[str]) -> List[str]:
    url_to_token = {}
    token_to_url = {}
    next_id = 1
    results = []
    for op, val in zip(operations, values):
        if op == "shorten":
            token = url_to_token.get(val)
            if token is None:
                token = _encode(next_id)
                next_id += 1
                url_to_token[val] = token
                token_to_url[token] = val
            results.append(token)
        else:
            results.append(token_to_url.get(val, ""))
    return results
