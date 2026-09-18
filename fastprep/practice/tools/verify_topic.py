#!/usr/bin/env python3
"""The gate every chapter has to pass before it ships.

A chapter is not "written" because a file exists. This checks the things a
reader would notice within a minute:

  * the fixed outline is present, in order - so every chapter reads the same
    way and you always know where the proof is;
  * every ```python run block actually runs in the same sandbox the app uses,
    exits cleanly and prints something;
  * there is a real proof block, at least one diagram, and self-checks;
  * every [[link]] points at a topic that exists;
  * length is in range, and no placeholder text survived.

  python3 tools/verify_topic.py                 # every article
  python3 tools/verify_topic.py binary-search   # one
  python3 tools/verify_topic.py --quiet --jobs 8
"""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)

import runner                                                  # noqa: E402
from canon import CANON                                        # noqa: E402

ARTICLES = os.path.join(ROOT, "topics", "articles")
SLUGS = {c[1] for c in CANON}
TITLES = {c[1]: c[2] for c in CANON}

# The outline every chapter follows, in this order.
REQUIRED = [
    "When you reach for it",
    "The idea",
    "Worked by hand",
    "Why it is correct",
    "What it costs",
    "The implementation",
    "Variants you will meet",
    "Recognising it in a statement",
    "Traps",
    "What to memorise",
    "Check yourself",
]
MIN_WORDS, MAX_WORDS = 2500, 7000
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME|lorem ipsum|XXX)\b", re.I)


def words(src: str) -> int:
    body = re.sub(r"(?s)```.*?```", " ", src)
    body = re.sub(r"(?s)<svg.*?</svg>", " ", body)
    return len(re.findall(r"[A-Za-z0-9'’-]+", body))


def snippets(src: str):
    out = []
    for m in re.finditer(r"(?ms)^```+([^\n]*)\n(.*?)^```+\s*$", src):
        info = m.group(1).split()
        out.append({"lang": info[0] if info else "", "run": "run" in info[1:],
                    "code": m.group(2)})
    return out


def check(slug: str, run_code: bool = True) -> dict:
    path = os.path.join(ARTICLES, slug + ".md")
    problems, notes = [], []
    if not os.path.isfile(path):
        return {"slug": slug, "ok": False, "problems": ["no article"], "words": 0}
    src = open(path, encoding="utf-8").read()

    heads = [m.group(1).strip() for m in re.finditer(r"(?m)^##\s+(.*)$", src)]
    missing = [h for h in REQUIRED if h not in heads]
    if missing:
        problems.append("missing sections: " + ", ".join(missing))
    else:
        order = [heads.index(h) for h in REQUIRED]
        if order != sorted(order):
            problems.append("sections are out of order")

    h1 = re.search(r"(?m)^#\s+(.*)$", src)
    if not h1:
        problems.append("no H1 title")
    elif TITLES.get(slug) and h1.group(1).strip() != TITLES[slug]:
        notes.append("H1 %r is not the canon title %r" % (h1.group(1).strip(), TITLES[slug]))
    if not re.search(r"(?m)^>\s+\S", src[:1500]):
        problems.append("no one-line lede (a '> ...' line under the title)")

    n = words(src)
    if n < MIN_WORDS:
        problems.append("only %d words (chapter depth starts at %d)" % (n, MIN_WORDS))
    if n > MAX_WORDS:
        notes.append("%d words is long" % n)

    if ":::proof" not in src:
        problems.append("no :::proof block")
    if "<svg" not in src:
        problems.append("no diagram")
    checks = src.count(":::check")
    if checks < 3:
        problems.append("only %d self-check questions (3 minimum)" % checks)
    if PLACEHOLDER.search(src):
        problems.append("placeholder text left in: %s" % PLACEHOLDER.search(src).group(0))

    for m in re.finditer(r"\[\[([a-z0-9-]+)(\|[^\]]+)?\]\]", src):
        if m.group(1) not in SLUGS:
            problems.append("[[%s]] is not a topic" % m.group(1))

    for m in re.finditer(r"(?s)<svg\b(.*?)>", src):
        if "viewBox" not in m.group(1):
            problems.append("an <svg> has no viewBox, so it will not scale")
            break

    snips = snippets(src)
    runnable = [s for s in snips if s["run"]]
    if not runnable:
        problems.append("no runnable code block (```python run)")
    if run_code:
        for i, s in enumerate(runnable):
            res = runner.run_snippet("", s["code"])
            if res.get("error"):
                problems.append("runnable block %d failed: %s"
                                % (i + 1, str(res["error"]).strip().split("\n")[-1][:160]))
            elif not (res.get("printed") or "").strip():
                problems.append("runnable block %d printed nothing" % (i + 1))
    for s in snips:
        if s["lang"] == "python" and not s["run"]:
            notes.append("a python block is not marked `run`")
            break

    return {"slug": slug, "ok": not problems, "problems": problems,
            "notes": notes, "words": n, "checks": checks,
            "runnable": len(runnable)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--no-run", action="store_true", help="skip the sandbox")
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    slugs = a.slugs
    if not slugs:
        slugs = sorted(f[:-3] for f in os.listdir(ARTICLES)
                       if f.endswith(".md")) if os.path.isdir(ARTICLES) else []
        if a.all:
            slugs = [c[1] for c in CANON]
    if not slugs:
        print("no articles yet")
        return 0

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, a.jobs)) as pool:
        for r in pool.map(lambda s: check(s, not a.no_run), slugs):
            results.append(r)
            if not a.quiet or not r["ok"]:
                mark = "ok  " if r["ok"] else "FAIL"
                print("%s %-32s %5d words, %d checks, %d runnable"
                      % (mark, r["slug"], r["words"], r.get("checks", 0), r.get("runnable", 0)))
                for p in r["problems"]:
                    print("       - " + p)
                if not a.quiet:
                    for nn in r.get("notes", []):
                        print("       . " + nn)

    good = [r for r in results if r["ok"]]
    print("\n%d/%d chapters pass" % (len(good), len(results)))
    if a.json:
        print(json.dumps(results))
    with open(os.path.join(ROOT, "topics", "VERIFIED.json"), "w") as fh:
        json.dump({"pass": sorted(r["slug"] for r in good),
                   "fail": {r["slug"]: r["problems"] for r in results if not r["ok"]}}, fh,
                  indent=1)
    return 0 if len(good) == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
