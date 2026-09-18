#!/usr/bin/env python3
"""Flag solutions that pass by memorising the examples rather than solving them.

Passing every visible example is the gate for keeping a solution, which creates
an obvious failure mode: return the expected answer when the input matches the
example. This looks for that.

    python3 tools/audit.py [problem-id ...]     # default: every stored solution

Heuristics, in order of how damning they are:
  * an example's expected output appears verbatim in the source
  * an example's input value appears verbatim in the source
  * the body is a chain of equality tests against literals with no loop or
    recursion at all

None of them is proof on its own - a legitimate lookup table can trip the
first two - so the output is a report to read, not a gate that deletes files.
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import fpdb

SOLUTIONS = os.path.join(HERE, "solutions")
TRIVIAL = {"", "0", "1", "-1", "[]", "true", "false", "null", '""', "0.0", "2", "3"}


def normalise(s: str) -> str:
    return re.sub(r"\s+", "", s or "")


def audit_one(bank, pid: str, path: str):
    d = bank.detail(pid)
    if not d:
        return ["no such problem"]
    with open(path, encoding="utf-8") as f:
        src = f.read()
    flat = normalise(src)
    flags = []

    for ex in d.get("examples") or []:
        out = (ex.get("outputText") or "").strip()
        if out and out not in TRIVIAL and len(out) >= 4 and normalise(out) in flat:
            flags.append("expected output %s appears verbatim" % out[:48])
        for item in ex.get("inputText") or []:
            val = (item.get("inputValue") or "").strip()
            if val and val not in TRIVIAL and len(val) >= 6 and normalise(val) in flat:
                flags.append("example input %s appears verbatim" % val[:48])

    body = re.sub(r"#.*", "", src)
    if path.endswith(".py"):
        has_flow = re.search(r"\b(for|while|sorted|sum|map|filter|recurs)\b", body) \
            or re.search(r"\w+\s*\(", body.split("def", 1)[-1])
        equality_returns = len(re.findall(r"if\s+[^:\n]*==[^:\n]*:\s*\n\s*return", body))
        if equality_returns >= 2 and not re.search(r"\b(for|while)\b", body):
            flags.append("%d literal equality branches and no loop" % equality_returns)
        if not has_flow:
            flags.append("no control flow at all")
    return flags


def main(argv) -> int:
    bank = fpdb.Bank()
    if argv:
        files = []
        for pid in argv:
            for ext in (".py", ".sql"):
                p = os.path.join(SOLUTIONS, pid + ext)
                if os.path.exists(p):
                    files.append(p)
    else:
        files = sorted(glob.glob(os.path.join(SOLUTIONS, "*.py")) +
                       glob.glob(os.path.join(SOLUTIONS, "*.sql")))
    suspicious = 0
    for path in files:
        pid = os.path.splitext(os.path.basename(path))[0]
        flags = audit_one(bank, pid, path)
        if flags:
            suspicious += 1
            print("SUSPECT %s" % pid)
            for f in flags[:4]:
                print("        %s" % f)
    print("\n%d solution(s) checked, %d flagged" % (len(files), suspicious))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
