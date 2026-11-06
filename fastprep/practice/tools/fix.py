#!/usr/bin/env python3
"""The repair worklist: which problems still need fixing, and is a repair valid.

    python3 tools/fix.py todo [-n 40] [--khatt] [--amazon]   what to fix next, most urgent first
    python3 tools/fix.py check <id> [<id> ...]               validate fixes/<id>.json
    python3 tools/fix.py check --all
    python3 tools/fix.py stats                               how much of the bank is repaired

A problem needs work when any of these hold:
  thin      the statement is under 400 characters, there is no screenshot, and nobody has reviewed it
  nosol     no verified reference solution (so no generated cases and no reference to compare)
  onecase   one published example and no generated cases
  nofix     no fixes/<id>.json (no hints, no "which pattern is this")

Order: problems the KHATT plan schedules (earliest week first), then Amazon OA problems
(most recently reported first), then everything else by how often it is reported.

To repair one: `python3 tools/brief.py <id>` for the problem, write solutions/<id>.py and
`python3 tools/verify.py <id>`, write fixes/<id>.json (see fixes.py for the shape), then
`python3 tools/fix.py check <id>`. After a batch: `tools/verify.py --all` and `tools/cases.py`.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import fixes, fpdb, solutions, topics


def _state(bank, pid, verified, khatt):
    d = bank.detail(pid)
    if not d or d.get("practiceFormat") == "tabular":
        return None
    text = re.sub(r"<[^>]+>", "", d.get("problemStatement") or "")
    fx = fixes.get(pid)
    flags = []
    # a short statement is only "thin" until someone has reviewed it: a repair
    # author rewrites it when it is unclear and leaves a short-but-exact one alone
    if len(text) < 400 and not d.get("sourceImages") and not fx:
        flags.append("thin")
    if pid not in verified:
        flags.append("nosol")
    if len(d.get("examples") or []) < 2 and not solutions.generated_cases(pid):
        flags.append("onecase")
    if not fx:
        flags.append("nofix")
    k = khatt.get(pid)
    stages = d.get("problemTypes") or []
    last = max(d.get("lastSeen") or [""])
    if k:
        rank = (0, k["week"], "SunMonTueWedThu".find(k.get("day", "")[:3]))
    elif d.get("company") == "Amazon" and "OA" in stages:
        rank = (1, -int(last.replace("-", "") or 0), 0)
    else:
        rank = (2, -(d.get("seenCount") or 0), -int(last.replace("-", "") or 0))
    return dict(id=pid, flags=flags, rank=rank, khatt=k, company=d.get("company"), title=d.get("title"))


def _verified():
    try:
        with open(os.path.join(HERE, "solutions", "VERIFIED.json")) as f:
            return {k for k, v in json.load(f)["problems"].items() if v.get("ok")}
    except (OSError, ValueError, KeyError):
        return set()


def todo(argv):
    n = 40
    if "-n" in argv:
        n = int(argv[argv.index("-n") + 1])
    bank = fpdb.Bank()
    khatt = {pid: fixes.khatt_for(pid) for pid in fixes.khatt_ids()}
    verified = _verified()
    ids = list(khatt) if "--khatt" in argv else bank.all_ids()
    rows = []
    for pid in ids:
        s = _state(bank, pid, verified, khatt)
        if not s or not s["flags"]:
            continue
        if "--amazon" in argv and s["company"] != "Amazon":
            continue
        rows.append(s)
    rows.sort(key=lambda r: r["rank"])
    for r in rows[:n]:
        where = ("W%02d %s" % (r["khatt"]["week"], r["khatt"]["day"])) if r["khatt"] else ""
        print("%-60s %-8s %s" % (r["id"], where, ",".join(r["flags"])))
    print("(%d need work%s)" % (len(rows), ", showing %d" % min(n, len(rows))), file=sys.stderr)
    return 0


def check(argv):
    known = {t["slug"] for t in topics.index().get("topics", [])}
    ids = argv
    if argv == ["--all"]:
        ids = sorted(f[:-5] for f in os.listdir(fixes.DIR) if f.endswith(".json") and f != "khatt.json")
    bad = 0
    for pid in ids:
        try:
            with open(fixes.path_for(pid)) as f:
                raw = json.load(f)
        except FileNotFoundError:
            raw = None
        except ValueError as e:
            print("%s: not valid JSON (%s)" % (pid, e)); bad += 1; continue
        errs = fixes.problems(raw, known)
        if errs:
            bad += 1
            print("%s: %s" % (pid, "; ".join(errs)))
        elif len(ids) < 10:
            print("%s: ok" % pid)
    if len(ids) >= 10:
        print("%d checked, %d bad" % (len(ids), bad))
    return 1 if bad else 0


def stats(argv):
    bank = fpdb.Bank()
    khatt = {pid: fixes.khatt_for(pid) for pid in fixes.khatt_ids()}
    verified = _verified()
    from collections import Counter
    for label, ids in (("KHATT plan", list(khatt)), ("whole bank", bank.all_ids())):
        c, n = Counter(), 0
        for pid in ids:
            s = _state(bank, pid, verified, khatt)
            if not s:
                continue
            n += 1
            c.update(s["flags"])
            if not s["flags"]:
                c["done"] += 1
        print("%-11s %5d problems: %5d fully repaired | thin %d, no verified solution %d, one case %d, no hints %d"
              % (label, n, c["done"], c["thin"], c["nosol"], c["onecase"], c["nofix"]))
    return 0


def main(argv):
    if not argv or argv[0] not in ("todo", "check", "stats"):
        print(__doc__)
        return 2
    return {"todo": todo, "check": check, "stats": stats}[argv[0]](argv[1:])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
