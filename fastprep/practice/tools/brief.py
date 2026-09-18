#!/usr/bin/env python3
"""Print everything needed to solve one problem, as plain text.

    python3 tools/brief.py <problem-id>

Used by the solution-writing agents: statement, constraints, the exact Python
signature the runner will call, and every visible example with its declared
types. Nothing else is needed - and nothing else should be guessed at.
"""
import json, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import fpdb, languages


def main(pid: str) -> int:
    bank = fpdb.Bank()
    d = bank.detail(pid)
    if not d:
        print("no problem with id %r" % pid, file=sys.stderr)
        return 1
    t = fpdb.html_to_text
    out = []
    out.append("PROBLEM %s" % d["id"])
    out.append("TITLE   %s" % d.get("title"))
    out.append("COMPANY %s | difficulty %s | stages %s | seen %s times, last %s"
               % (d.get("company"), d.get("difficulty"),
                  ", ".join(d.get("problemTypes") or []), d.get("seenCount"),
                  (d.get("lastSeen") or [None])[0]))
    out.append("FORMAT  %s" % d.get("practiceFormat"))
    out.append("")
    out.append("STATEMENT")
    out.append(t(d.get("problemStatement") or ""))
    if d.get("constraints"):
        out.append("")
        out.append("CONSTRAINTS")
        out.append(t(d["constraints"]))
    if d.get("sourceNote"):
        out.append("")
        out.append("SOURCE NOTE: %s" % d["sourceNote"])

    if d.get("practiceFormat") == "tabular":
        tab = d.get("tabular") or {}
        out.append("")
        out.append("TABLES")
        for tbl in tab.get("inputSchema") or []:
            cols = ", ".join("%s %s" % (c["name"], c["type"]) for c in tbl["columns"])
            out.append("  %s(%s)" % (tbl["name"], cols))
        rc = tab.get("resultContract") or {}
        out.append("RESULT  %s | rowOrder=%s | tolerance=%s"
                   % (", ".join("%s %s" % (c["name"], c["type"]) for c in rc.get("columns") or []),
                      rc.get("rowOrder"), rc.get("numericTolerance")))
        out.append("")
        out.append("VISIBLE CASES")
        out.append(json.dumps(tab.get("visibleCases") or [], indent=1)[:4000])
        out.append("")
        out.append("WRITE: a single SQL SELECT (SQLite dialect) into "
                   "solutions/%s.sql" % d["id"])
    else:
        out.append("")
        out.append("PYTHON SIGNATURE (the runner calls exactly this)")
        out.append(languages.python_starter(d).strip())
        out.append("")
        out.append("VISIBLE EXAMPLES")
        for i, ex in enumerate(d.get("examples") or [], 1):
            out.append("  example %s" % (ex.get("id") or i))
            for item in ex.get("inputText") or []:
                out.append("    %s (%s) = %s" % (item.get("inputName"), item.get("inputType"),
                                                 item.get("inputValue")))
            out.append("    -> expected (%s) = %s" % (ex.get("outputType"), ex.get("outputText")))
            if ex.get("explanation"):
                out.append("    why: %s" % t(ex["explanation"]).replace("\n", " ")[:400])
        out.append("")
        out.append("WRITE: python into solutions/%s.py, then verify with:" % d["id"])
        out.append("  python3 tools/verify.py %s" % d["id"])
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]) if len(sys.argv) > 1 else 2)
