# Line-grouping block parser plus a recursive scan that pairs ** / ~~ delimiters inside each block.


def _inline(s: str) -> str:
    out = []
    i = 0
    n = len(s)
    while i < n:
        tok = s[i:i + 2]
        if tok == "**" or tok == "~~":
            j = s.find(tok, i + 2)
            if j == -1:
                out.append(tok)
                i += 2
            else:
                tag = "strong" if tok == "**" else "del"
                out.append("<" + tag + ">")
                out.append(_inline(s[i + 2:j]))
                out.append("</" + tag + ">")
                i = j + 2
        else:
            out.append(s[i])
            i += 1
    return "".join(out)


def renderLightweightMarkup(text: str) -> str:
    if not text:
        return ""
    lines = text.split("\n")
    blocks = []          # list of (kind, [lines])
    for line in lines:
        if line.strip() == "":
            blocks.append(None)          # boundary marker
            continue
        kind = "quote" if line.startswith(">") else "para"
        if kind == "quote":
            body = line[1:]
            if body.startswith(" "):
                body = body[1:]
        else:
            body = line
        if blocks and blocks[-1] is not None and blocks[-1][0] == kind:
            blocks[-1][1].append(body)
        else:
            blocks.append((kind, [body]))

    parts = []
    for b in blocks:
        if b is None:
            continue
        kind, body_lines = b
        content = _inline("<br>".join(body_lines))
        if kind == "quote":
            parts.append("<blockquote>" + content + "</blockquote>")
        else:
            parts.append("<p>" + content + "</p>")
    return "".join(parts)
