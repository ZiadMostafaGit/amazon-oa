"""A small, strict Markdown renderer for the topic articles.

The articles are written by hand (and by agents) against a fixed dialect, so a
full CommonMark implementation would be a dependency with no payoff. This
renders exactly the constructs the dialect allows and nothing else:

    # .. ######        headings, each given a stable anchor id
    ```python run     fenced code; `run` marks it executable in the sandbox
    :::proof          callouts: proof, note, warn, aside
    :::check          a self-check question; the answer after a `--` line is
                      hidden until the reader asks for it
    > quote           blockquote
    - / 1.            lists, one level of nesting via two-space indent
    | a | b |         tables with a --- separator row
    ---               horizontal rule
    <svg ...>         raw HTML, passed through verbatim (diagrams)

Inline: `code`, **bold**, *italic*, [text](url), and [[topic-slug]] /
[[topic-slug|text]] which becomes a link into the study space.

Everything that is not one of those is escaped, so an article cannot smuggle a
<script> in through a paragraph.
"""

from __future__ import annotations

import html
import re

RAW_START = re.compile(r"^\s*<(svg|figure|table|div)\b", re.I)
CALLOUTS = {"proof", "note", "warn", "aside", "check", "example"}


def slugify(text: str) -> str:
    s = re.sub(r"<[^>]+>", "", text).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "section"


def inline(text: str, topic_href=None) -> str:
    out = html.escape(text, quote=False)

    codes: list[str] = []

    def stash(m):
        # the text is already escaped: escaping again would show "&amp;gt;"
        codes.append(m.group(1))
        return "\x00%d\x00" % (len(codes) - 1)

    # `code` is stashed first so nothing below reformats its contents
    out = re.sub(r"`([^`]+)`", stash, out)
    out = re.sub(r"\[\[([a-z0-9-]+)(?:\|([^\]]+))?\]\]",
                 lambda m: '<a class="tlink" href="%s">%s</a>' % (
                     (topic_href or (lambda s: "#" + s))(m.group(1)),
                     m.group(2) or m.group(1).replace("-", " ")), out)
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)",
                 lambda m: '<a href="%s" target="_blank" rel="noopener">%s</a>'
                 % (html.escape(m.group(2), quote=True), m.group(1)), out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", out)
    out = re.sub(r"\x00(\d+)\x00", lambda m: "<code>%s</code>" % codes[int(m.group(1))], out)
    return out


class _Doc:
    def __init__(self, topic_href=None):
        self.parts: list[str] = []
        self.toc: list[dict] = []
        self.snippets: list[dict] = []
        self.checks = 0
        self.topic_href = topic_href

    def inline(self, s):
        return inline(s, self.topic_href)


def _lines(src: str) -> list[str]:
    return src.replace("\r\n", "\n").replace("\t", "    ").split("\n")


def _render_block(lines: list[str], doc: _Doc, depth: int = 0) -> None:
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            anchor = slugify(text)
            base = anchor
            k = 2
            while any(t["id"] == anchor for t in doc.toc):
                anchor = "%s-%d" % (base, k)
                k += 1
            doc.toc.append({"id": anchor, "level": level, "text": re.sub(r"[*`]", "", text)})
            doc.parts.append('<h%d id="%s">%s</h%d>' % (level, anchor, doc.inline(text), level))
            i += 1
            continue

        m = re.match(r"^```+\s*(.*)$", line)
        if m:
            info = m.group(1).strip().split()
            lang = info[0] if info else ""
            runnable = "run" in info[1:]
            body, i = [], i + 1
            while i < n and not re.match(r"^```+\s*$", lines[i]):
                body.append(lines[i])
                i += 1
            i += 1
            code = "\n".join(body)
            idx = len(doc.snippets)
            doc.snippets.append({"lang": lang or "text", "run": runnable, "code": code})
            doc.parts.append(
                '<div class="snippet%s" data-snippet="%d" data-lang="%s"%s>'
                '<pre><code>%s</code></pre></div>'
                % (" runnable" if runnable else "", idx, html.escape(lang or "text", True),
                   ' data-run="1"' if runnable else "",
                   html.escape(code, quote=False)))
            continue

        m = re.match(r"^:::\s*([a-z]+)\s*(.*)$", line)
        if m and m.group(1) in CALLOUTS:
            kind, title = m.group(1), m.group(2).strip()
            body, i, level = [], i + 1, 1
            while i < n:
                if re.match(r"^:::\s*[a-z]+", lines[i]):
                    level += 1
                elif lines[i].strip() == ":::":
                    level -= 1
                    if level == 0:
                        i += 1
                        break
                body.append(lines[i])
                i += 1
            if kind == "check":
                doc.checks += 1
                if any(l.strip() == "--" for l in body):
                    cut = [k for k, l in enumerate(body) if l.strip() == "--"][0]
                    q, a = body[:cut], body[cut + 1:]
                else:
                    q, a = body, []
                qd, ad = _Doc(doc.topic_href), _Doc(doc.topic_href)
                _render_block(q, qd, depth + 1)
                _render_block(a, ad, depth + 1)
                doc.snippets.extend(qd.snippets + ad.snippets)
                doc.parts.append(
                    '<div class="check" data-check="%d"><div class="q">%s</div>'
                    '<button class="reveal" type="button">Show answer</button>'
                    '<div class="a" hidden>%s</div></div>'
                    % (doc.checks, "".join(qd.parts), "".join(ad.parts)))
            else:
                inner = _Doc(doc.topic_href)
                _render_block(body, inner, depth + 1)
                doc.snippets.extend(inner.snippets)
                doc.toc.extend(inner.toc)
                doc.parts.append(
                    '<aside class="callout %s">%s%s</aside>'
                    % (kind,
                       '<div class="ctitle">%s</div>' % doc.inline(title or kind.title()),
                       "".join(inner.parts)))
            continue

        if RAW_START.match(line):
            tag = RAW_START.match(line).group(1).lower()
            body, level = [], 0
            while i < n:
                body.append(lines[i])
                level += len(re.findall(r"<%s\b" % tag, lines[i], re.I))
                level -= len(re.findall(r"</%s>" % tag, lines[i], re.I))
                i += 1
                if level <= 0:
                    break
            raw = "\n".join(body)
            raw = re.sub(r"(?is)<script.*?</script>", "", raw)
            raw = re.sub(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)", "", raw)
            doc.parts.append(raw)
            continue

        if line.lstrip().startswith(">"):
            body = []
            while i < n and (lines[i].lstrip().startswith(">") or
                             (body and lines[i].strip())):
                body.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            inner = _Doc(doc.topic_href)
            _render_block(body, inner, depth + 1)
            doc.snippets.extend(inner.snippets)
            doc.parts.append("<blockquote>%s</blockquote>" % "".join(inner.parts))
            continue

        if re.match(r"^\s*\|.*\|\s*$", line) and i + 1 < n and \
                re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            def cells(row):
                return [c.strip() for c in row.strip().strip("|").split("|")]
            head = cells(line)
            i += 2
            rows = []
            while i < n and re.match(r"^\s*\|.*\|\s*$", lines[i]):
                rows.append(cells(lines[i]))
                i += 1
            doc.parts.append(
                "<table><thead><tr>%s</tr></thead><tbody>%s</tbody></table>"
                % ("".join("<th>%s</th>" % doc.inline(c) for c in head),
                   "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % doc.inline(c)
                                                   for c in r) for r in rows)))
            continue

        if re.match(r"^\s*(---|\*\*\*)\s*$", line):
            doc.parts.append("<hr>")
            i += 1
            continue

        m = re.match(r"^(\s*)([-*+]|\d+[.)])\s+", line)
        if m:
            ordered = not m.group(2)[0] in "-*+"
            items, base_indent = [], len(m.group(1))
            while i < n:
                mm = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", lines[i])
                if mm and len(mm.group(1)) >= base_indent:
                    if len(mm.group(1)) > base_indent:
                        items[-1].append(lines[i][base_indent:])
                    else:
                        items.append([mm.group(3)])
                    i += 1
                elif lines[i].strip() and items and lines[i].startswith(" " * (base_indent + 2)):
                    items[-1].append(lines[i].strip())
                    i += 1
                else:
                    break
            out = []
            for item in items:
                sub = [l for l in item[1:] if re.match(r"^\s*([-*+]|\d+[.)])\s+", l)]
                text = " ".join(l for l in item if l not in sub)
                piece = doc.inline(text.strip())
                if sub:
                    inner = _Doc(doc.topic_href)
                    _render_block(sub, inner, depth + 1)
                    piece += "".join(inner.parts)
                out.append("<li>%s</li>" % piece)
            tag = "ol" if ordered else "ul"
            doc.parts.append("<%s>%s</%s>" % (tag, "".join(out), tag))
            continue

        body = []
        while i < n and lines[i].strip() and not re.match(
                r"^(#{1,6}\s|```|:::|>|\s*([-*+]|\d+[.)])\s|\s*\|)", lines[i]) \
                and not RAW_START.match(lines[i]):
            body.append(lines[i].strip())
            i += 1
        if body:
            doc.parts.append("<p>%s</p>" % doc.inline(" ".join(body)))
        else:
            i += 1


def render(src: str, topic_href=None) -> dict:
    """-> {html, toc, snippets, checks}"""
    doc = _Doc(topic_href)
    _render_block(_lines(src), doc)
    return {"html": "".join(doc.parts), "toc": doc.toc,
            "snippets": doc.snippets, "checks": doc.checks}
